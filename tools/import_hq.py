#!/usr/bin/env python3
# Rebuilds the "Knowledge Graph/" and "Reference/" folders from a checkout of the hq repo.
# Usage: python3 tools/import_hq.py ../hq
#
# Everything this script writes is regenerated on each run, so do not hand-edit
# files under "Knowledge Graph/" or "Reference/hq docs/". Put your own notes elsewhere.

import posixpath
import re
import shutil
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_FOLDER = VAULT_ROOT / "Knowledge Graph"
DOCS_FOLDER = VAULT_ROOT / "Reference" / "hq docs"
PUBLIC_SITE = "https://robbiepalmer.me"
HQ_GITHUB = "https://github.com/Robbie-Palmer/hq/blob/main/"

AGENTIC_PROJECTS = [
    "agent-coordinator",
    "agent-first-writing",
    "agent-friendly-remote-development",
    "agentic-code-review",
    "work-graph",
]

INITIATIVES = [
    "semi-autonomous-software-development",
]

# Individual decision records from projects that are not agentic as a whole.
EXTRA_DECISIONS = [
    "personal-knowledge-graph/adrs/009-code-rabbit.mdx",
    "personal-knowledge-graph/adrs/012-claude-code.mdx",
    "personal-knowledge-graph/adrs/027-ccpm.mdx",
    "personal-knowledge-graph/adrs/033-content-graph-indexes.mdx",
    "personal-knowledge-graph/adrs/038-content-graph.mdx",
    "personal-knowledge-graph/adrs/041-gemini-code-assist.mdx",
    "personal-knowledge-graph/adrs/042-greptile.mdx",
    "personal-knowledge-graph/adrs/043-codex.mdx",
    "personal-knowledge-graph/adrs/044-codex-code-review.mdx",
    "personal-knowledge-graph/adrs/045-qodo.mdx",
    "personal-knowledge-graph/adrs/059-product-decision-records.mdx",
    "homelab/adrs/011-basic-memory-silverbullet-agentic-knowledge-base.mdx",
    "homelab/pdrs/007-keep-private-knowledge-agent-operable.mdx",
]

BLOG_POSTS = [
    "2026-08-18-crossing-the-chasm-with-ai-platform-teams.mdx",
]

PLAIN_DOCS = [
    "docs/work-graph-mvp.md",
    "docs/runbooks/agent-coordinator-hq-delivery.md",
    "packages/agent-coordinator-domain/docs/compatibility-examples.md",
    "packages/agent-coordinator-domain/docs/execution-telemetry.md",
    "packages/agent-coordinator-domain/docs/worker-adapters.md",
    "ai-review/README.md",
]

# Frontmatter keys copied as they are. Everything else is dropped or turned into links.
KEPT_KEYS = ["description", "date", "status", "decision_date", "source_url"]

# Frontmatter keys whose values point at other notes.
LINK_KEYS = {
    "related_ideas": "idea",
    "ideas": "idea",
    "initiatives": "initiative",
    "supersedes": "decision",
    "informed_by_adrs": "decision",
    "implements_product_decisions": "product-decision",
}


class Note:
    def __init__(self, source_path, kind, key, folder):
        self.source_path = source_path
        self.kind = kind
        self.key = key
        self.folder = folder
        self.frontmatter = {}
        self.body = ""
        self.name = ""


def read_frontmatter(text):
    # Returns (fields, body). Only understands the flat shapes used in hq content:
    #   key: "value"
    #   key: ["a", "b"]
    #   key:
    #     - "a"
    # Nested mappings (like platform_layers) are skipped.
    if not text.startswith("---\n"):
        return {}, text

    end = text.index("\n---", 4)
    header = text[4:end]
    body = text[end + 4:].lstrip("\n")

    fields = {}
    current_list_key = None
    for line in header.split("\n"):
        if line.startswith("  - ") and current_list_key is not None:
            fields[current_list_key].append(unquote(line[4:]))
            continue

        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if match is None:
            current_list_key = None
            continue

        key = match.group(1)
        value = match.group(2).strip()
        if value == "":
            fields[key] = []
            current_list_key = key
        elif value.startswith("["):
            inner = value.strip("[]")
            items = []
            for item in inner.split(","):
                if item.strip() != "":
                    items.append(unquote(item))
            fields[key] = items
            current_list_key = None
        else:
            fields[key] = unquote(value)
            current_list_key = None

    return fields, body


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def safe_file_name(title):
    # Obsidian refuses these characters in note names.
    name = title.replace(": ", " - ")
    for character in ':*?"<>|\\/#^[]':
        name = name.replace(character, "")
    return name.strip()


def collect_notes(hq_root):
    content = hq_root / "ui" / "content"
    notes = []

    for path in sorted((content / "ideas").glob("*.mdx")):
        notes.append(Note(path, "idea", path.stem, "Ideas"))

    for slug in INITIATIVES:
        path = content / "initiatives" / (slug + ".mdx")
        notes.append(Note(path, "initiative", slug, "Initiatives"))

    philosophy = content / "projects" / "building-philosophy.mdx"
    notes.append(Note(philosophy, "philosophy", "building-philosophy", "Philosophy"))

    for slug in AGENTIC_PROJECTS:
        project_folder = content / "projects" / slug
        notes.append(Note(project_folder / "index.mdx", "project", slug, "Projects/" + slug))

        for path in sorted((project_folder / "adrs").glob("*.mdx")):
            key = slug + ":" + path.stem
            notes.append(Note(path, "decision", key, "Projects/" + slug + "/ADRs"))

        for path in sorted((project_folder / "pdrs").glob("*.mdx")):
            key = slug + ":" + path.stem
            notes.append(Note(path, "product-decision", key, "Projects/" + slug + "/PDRs"))

    for relative in EXTRA_DECISIONS:
        path = content / "projects" / relative
        project_slug, record_type, file_name = relative.split("/")
        key = project_slug + ":" + Path(file_name).stem
        if record_type == "adrs":
            kind = "decision"
        else:
            kind = "product-decision"
        notes.append(Note(path, kind, key, "Projects/" + project_slug))

    for file_name in BLOG_POSTS:
        path = content / "blog" / file_name
        slug = Path(file_name).stem[len("2026-08-18-"):]
        notes.append(Note(path, "blog", slug, "Blog"))

    return notes


def assign_names(notes):
    used_names = {}
    for note in notes:
        text = note.source_path.read_text(encoding="utf-8")
        note.frontmatter, note.body = read_frontmatter(text)
        title = note.frontmatter.get("title", note.key)
        name = safe_file_name(title)

        if name in used_names:
            project_slug = note.key.split(":")[0]
            name = name + " (" + project_slug + ")"
        if name in used_names:
            raise SystemExit("Two notes would share the name: " + name)

        used_names[name] = note
        note.name = name


def build_lookup(notes):
    # Maps (kind, key) to a note so links can be resolved.
    lookup = {}
    for note in notes:
        lookup[(note.kind, note.key)] = note
    return lookup


def find_link_target(lookup, kind, key):
    if kind == "decision" or kind == "product-decision":
        for candidate_kind in ["decision", "product-decision"]:
            if (candidate_kind, key) in lookup:
                return lookup[(candidate_kind, key)]
        return None
    return lookup.get((kind, key))


def convert_site_link(lookup, url):
    # Turns a site-relative URL like /ideas/foo into a note name, or returns None.
    path = url.split("#")[0].split("?")[0].strip("/")
    parts = path.split("/")

    if len(parts) == 2 and parts[0] == "ideas":
        return find_link_target(lookup, "idea", parts[1])
    if len(parts) == 2 and parts[0] == "initiatives":
        return find_link_target(lookup, "initiative", parts[1])
    if len(parts) == 1 and parts[0] == "building-philosophy":
        return find_link_target(lookup, "philosophy", "building-philosophy")
    if len(parts) == 2 and parts[0] == "projects":
        return find_link_target(lookup, "project", parts[1])
    if len(parts) == 4 and parts[0] == "projects":
        key = parts[1] + ":" + parts[3]
        return find_link_target(lookup, "decision", key)
    return None


def rewrite_body_links(lookup, body):
    def replace(match):
        text = match.group(1)
        url = match.group(2)
        target = convert_site_link(lookup, url)
        if target is not None:
            return "[[" + target.name + "|" + text + "]]"
        return "[" + text + "](" + PUBLIC_SITE + url + ")"

    return re.sub(r"\[([^\]]+)\]\((/[^)\s]*)\)", replace, body)


def rewrite_mermaid(body):
    # <Mermaid chart={`...`} /> becomes a fenced mermaid block, which Obsidian renders.
    # Extra attributes such as className are dropped.
    pattern = re.compile(r"<Mermaid\s+chart=\{`(.*?)`\}.*?/>", re.DOTALL)
    return pattern.sub(lambda match: "```mermaid\n" + match.group(1).strip() + "\n```", body)


def rewrite_site_components(body):
    # Interactive site components cannot render in Obsidian. Point at the live page instead.
    replacement = "_Interactive graph: open " + PUBLIC_SITE + "/projects or use the Obsidian graph view._"
    return body.replace("<KnowledgeGraph />", replacement)


def build_links_section(lookup, note):
    lines = []
    for key, kind in LINK_KEYS.items():
        values = note.frontmatter.get(key, [])
        if isinstance(values, str):
            values = [values]
        for value in values:
            target = find_link_target(lookup, kind, value)
            label = key.replace("_", " ")
            if target is not None:
                lines.append("- " + label + ": [[" + target.name + "]]")
            else:
                lines.append("- " + label + ": " + value + " (not imported)")

    if note.kind in ("decision", "product-decision"):
        project_slug = note.key.split(":")[0]
        project = find_link_target(lookup, "project", project_slug)
        if project is not None:
            lines.append("- project: [[" + project.name + "]]")

    if len(lines) == 0:
        return ""
    return "\n\n## Links\n\n" + "\n".join(lines) + "\n"


def site_url(note):
    if note.kind == "idea":
        return PUBLIC_SITE + "/ideas/" + note.key
    if note.kind == "initiative":
        return PUBLIC_SITE + "/initiatives/" + note.key
    if note.kind == "project":
        return PUBLIC_SITE + "/projects/" + note.key
    if note.kind == "philosophy":
        return PUBLIC_SITE + "/building-philosophy"
    if note.kind == "blog":
        return PUBLIC_SITE + "/blog/" + note.key
    project_slug, record = note.key.split(":")
    if note.kind == "decision":
        return PUBLIC_SITE + "/projects/" + project_slug + "/adrs/" + record
    return PUBLIC_SITE + "/projects/" + project_slug + "/pdrs/" + record


def yaml_quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_note(lookup, note):
    title = note.frontmatter.get("title", note.key)
    lines = ["---"]
    lines.append("title: " + yaml_quote(title))
    lines.append("type: " + note.kind)
    for key in KEPT_KEYS:
        value = note.frontmatter.get(key)
        if isinstance(value, str) and value != "":
            lines.append(key + ": " + yaml_quote(value))
    tech_stack = note.frontmatter.get("tech_stack", [])
    if isinstance(tech_stack, list) and len(tech_stack) > 0:
        lines.append("tech_stack:")
        for technology in tech_stack:
            lines.append("  - " + yaml_quote(technology))
    lines.append("tags:")
    lines.append("  - hq")
    lines.append("  - " + note.kind)
    lines.append("source: " + yaml_quote(site_url(note)))
    lines.append("author: Robbie Palmer")
    lines.append("---")
    lines.append("")
    lines.append("")

    body = rewrite_mermaid(note.body)
    body = rewrite_site_components(body)
    body = rewrite_body_links(lookup, body)
    if not body.lstrip().startswith("# "):
        body = "# " + title + "\n\n" + body

    return "\n".join(lines) + body.rstrip() + "\n" + build_links_section(lookup, note)


def content_path_to_site_url(repo_path):
    # ui/content/projects/x/adrs/001-y.mdx -> /projects/x/adrs/001-y
    # ui/content/projects/x/index.mdx      -> /projects/x
    prefix = "ui/content/"
    if not repo_path.startswith(prefix) or not repo_path.endswith(".mdx"):
        return None
    site_path = repo_path[len(prefix):-len(".mdx")]
    if site_path.endswith("/index"):
        site_path = site_path[:-len("/index")]
    return "/" + site_path


def rewrite_repo_links(lookup, text, relative_doc):
    # Relative links in hq docs point at other files in the hq repo. Imported notes
    # become wikilinks and everything else points at GitHub.
    doc_folder = posixpath.dirname(relative_doc)

    def replace(match):
        label = match.group(1)
        url = match.group(2)
        is_external = url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:")
        if is_external or url.startswith("#") or url.startswith("/"):
            return match.group(0)

        file_part = url.split("#")[0]
        repo_path = posixpath.normpath(posixpath.join(doc_folder, file_part))
        site_url = content_path_to_site_url(repo_path)
        if site_url is not None:
            target = convert_site_link(lookup, site_url)
            if target is not None:
                return "[[" + target.name + "|" + label + "]]"
            return "[" + label + "](" + PUBLIC_SITE + site_url + ")"
        return "[" + label + "](" + HQ_GITHUB + repo_path + ")"

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", replace, text)
    return rewrite_body_links(lookup, text)


def import_plain_docs(hq_root, lookup):
    for relative in PLAIN_DOCS:
        source = hq_root / relative
        if relative == "ai-review/README.md":
            target_name = "ai-review README.md"
        else:
            target_name = Path(relative).name
        text = rewrite_repo_links(lookup, source.read_text(encoding="utf-8"), relative)
        header = "---\n"
        header += "type: reference\n"
        header += "tags:\n  - hq\n  - reference\n"
        header += "source: " + yaml_quote("https://github.com/Robbie-Palmer/hq/blob/main/" + relative) + "\n"
        header += "author: Robbie Palmer\n"
        header += "---\n\n"
        (DOCS_FOLDER / target_name).write_text(header + text, encoding="utf-8")


KIND_HEADINGS = [
    ("initiative", "Initiatives"),
    ("philosophy", "Philosophy"),
    ("project", "Projects"),
    ("decision", "Architecture decision records"),
    ("product-decision", "Product decision records"),
    ("idea", "Ideas"),
    ("blog", "Blog posts"),
]


def render_index(notes):
    lines = ["---"]
    lines.append('title: "Knowledge Graph Index"')
    lines.append("type: index")
    lines.append("tags:")
    lines.append("  - hq")
    lines.append("  - index")
    lines.append("---")
    lines.append("")
    lines.append("# Knowledge graph index")
    lines.append("")
    lines.append("Generated by `tools/import_hq.py`. Every note imported from hq, grouped by type.")
    lines.append("See [[hq Overview]] for what these are and where they came from.")

    for kind, heading in KIND_HEADINGS:
        names = []
        for note in notes:
            if note.kind == kind:
                names.append(note.name)
        if len(names) == 0:
            continue
        names.sort()
        lines.append("")
        lines.append("## " + heading)
        lines.append("")
        for name in names:
            lines.append("- [[" + name + "]]")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 tools/import_hq.py <path to hq checkout>")
    hq_root = Path(sys.argv[1]).resolve()

    notes = collect_notes(hq_root)
    assign_names(notes)
    lookup = build_lookup(notes)

    # Check every source before deleting anything, so a bad checkout leaves the vault as it was.
    missing = []
    for relative in PLAIN_DOCS:
        if not (hq_root / relative).is_file():
            missing.append(relative)
    if len(missing) > 0:
        raise SystemExit("Missing from the hq checkout: " + ", ".join(missing))

    if GRAPH_FOLDER.exists():
        shutil.rmtree(GRAPH_FOLDER)
    if DOCS_FOLDER.exists():
        shutil.rmtree(DOCS_FOLDER)
    DOCS_FOLDER.mkdir(parents=True)

    for note in notes:
        folder = GRAPH_FOLDER / note.folder
        folder.mkdir(parents=True, exist_ok=True)
        (folder / (note.name + ".md")).write_text(render_note(lookup, note), encoding="utf-8")

    (GRAPH_FOLDER / "Knowledge Graph Index.md").write_text(render_index(notes), encoding="utf-8")
    import_plain_docs(hq_root, lookup)
    print("Imported " + str(len(notes)) + " graph notes and " + str(len(PLAIN_DOCS)) + " docs.")


if __name__ == "__main__":
    main()
