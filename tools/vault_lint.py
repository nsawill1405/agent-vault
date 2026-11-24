#!/usr/bin/env python3
# Checks that the vault is consistent. Usage: python3 tools/vault_lint.py [vault folder]
#
# Rules:
#   frontmatter       every note starts with YAML frontmatter containing "type:" and "tags:"
#   broken-link       every [[wikilink]] points at a note that exists
#   duplicate-name    two notes share a file name, which makes wikilinks ambiguous
#   bad-file-name     file name contains a character Obsidian does not allow
#   prose             hand-written notes avoid the AI tells listed in Skills/Unslop.md

import re
import sys
from pathlib import Path

SKIPPED_FOLDERS = {".git", ".github", ".obsidian", "tools", "node_modules"}
ROOT_FILES_WITHOUT_FRONTMATTER = {"README.md", "AGENTS.md", "CLAUDE.md"}

# Hand-written notes. Imported notes keep their author's wording, so they are not checked.
PROSE_CHECKED_PREFIXES = [
    "William/",
    "Home.md",
    "Skills/PR Review Loop.md",
    "Skills/Style Linter.md",
    "Reference/hq Overview.md",
]

BANNED_CHARACTERS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u201c": "curly quote",
    "\u201d": "curly quote",
    "\u2018": "curly quote",
    "\u2019": "curly quote",
}

BANNED_WORDS = [
    "delve",
    "tapestry",
    "testament",
    "seamless",
    "seamlessly",
    "leverage",
    "utilize",
    "pivotal",
    "vibrant",
    "showcase",
    "crucial",
    "robust",
]

FORBIDDEN_FILE_NAME_CHARACTERS = '*"<>:|?#^[]\\'

WIKILINK_PATTERN = re.compile(r"!?\[\[([^\]]+)\]\]")


class Finding:
    def __init__(self, path, line, rule, message):
        self.path = path
        self.line = line
        self.rule = rule
        self.message = message

    def __str__(self):
        return str(self.path) + ":" + str(self.line) + ": " + self.rule + " " + self.message


def collect_notes(vault_root):
    notes = []
    for path in sorted(vault_root.rglob("*.md")):
        relative = path.relative_to(vault_root)
        if any(part in SKIPPED_FOLDERS for part in relative.parts):
            continue
        notes.append(relative)
    return notes


def strip_code(text):
    # Blanks fenced blocks and inline code but keeps line numbers the same.
    lines = text.split("\n")
    inside_fence = False
    result = []
    for line in lines:
        if line.strip().startswith("```"):
            inside_fence = not inside_fence
            result.append("")
            continue
        if inside_fence:
            result.append("")
            continue
        result.append(re.sub(r"`[^`]*`", "", line))
    return result


def check_frontmatter(relative, text):
    if relative.as_posix() in ROOT_FILES_WITHOUT_FRONTMATTER:
        return []
    if not text.startswith("---\n"):
        return [Finding(relative, 1, "frontmatter", "missing YAML frontmatter")]

    end = text.find("\n---", 4)
    if end == -1:
        return [Finding(relative, 1, "frontmatter", "frontmatter is not closed")]

    header_lines = text[4:end].split("\n")
    findings = []
    for required_key in ["type", "tags"]:
        has_key = False
        for line in header_lines:
            if line.startswith(required_key + ":"):
                has_key = True
        if not has_key:
            findings.append(Finding(relative, 1, "frontmatter", "missing '" + required_key + "'"))
    return findings


def link_target(raw_link):
    # [[Note#Heading|Label]] -> "Note"
    target = raw_link.split("|")[0]
    target = target.split("#")[0]
    return target.strip()


def check_links(relative, code_free_lines, note_names, note_paths):
    findings = []
    for line_number, line in enumerate(code_free_lines, start=1):
        for match in WIKILINK_PATTERN.finditer(line):
            target = link_target(match.group(1))
            if target == "":
                continue
            if "/" in target:
                path_target = target if target.endswith(".md") else target + ".md"
                if path_target in note_paths:
                    continue
            elif target in note_names:
                continue
            findings.append(Finding(relative, line_number, "broken-link", "[[" + target + "]] has no matching note"))
    return findings


def is_prose_checked(relative):
    posix = relative.as_posix()
    for prefix in PROSE_CHECKED_PREFIXES:
        if posix.startswith(prefix):
            return True
    return False


def check_prose(relative, code_free_lines):
    findings = []
    for line_number, line in enumerate(code_free_lines, start=1):
        for character, label in BANNED_CHARACTERS.items():
            if character in line:
                findings.append(Finding(relative, line_number, "prose", label + "; see [[Unslop]]"))

        lowered = line.lower()
        for word in BANNED_WORDS:
            if re.search(r"\b" + word + r"\b", lowered):
                findings.append(Finding(relative, line_number, "prose", "'" + word + "'; use a plainer word"))
    return findings


def check_file_name(relative):
    for character in FORBIDDEN_FILE_NAME_CHARACTERS:
        if character in relative.name:
            return [Finding(relative, 1, "bad-file-name", "contains '" + character + "'")]
    return []


def lint_vault(vault_root):
    notes = collect_notes(vault_root)
    findings = []

    names_to_paths = {}
    for relative in notes:
        names_to_paths.setdefault(relative.stem, []).append(relative)
    for name, paths in names_to_paths.items():
        if len(paths) > 1:
            listed = ", ".join(path.as_posix() for path in paths)
            findings.append(Finding(paths[0], 1, "duplicate-name", "'" + name + "' is used by " + listed))

    note_names = set(names_to_paths.keys())
    note_paths = set(relative.as_posix() for relative in notes)

    for relative in notes:
        text = (vault_root / relative).read_text(encoding="utf-8")
        code_free_lines = strip_code(text)
        findings.extend(check_file_name(relative))
        findings.extend(check_frontmatter(relative, text))
        findings.extend(check_links(relative, code_free_lines, note_names, note_paths))
        if is_prose_checked(relative):
            findings.extend(check_prose(relative, code_free_lines))

    return findings


def main():
    if len(sys.argv) > 1:
        vault_root = Path(sys.argv[1])
    else:
        vault_root = Path(__file__).resolve().parent.parent

    findings = lint_vault(vault_root)
    for finding in findings:
        print(finding)

    if len(findings) > 0:
        print(str(len(findings)) + " vault finding(s).")
        sys.exit(1)
    print("Vault is clean.")


if __name__ == "__main__":
    main()
