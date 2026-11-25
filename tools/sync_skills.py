#!/usr/bin/env python3
# Exports Obsidian skill notes in Skills/*.md to Devin's SKILL.md directory layout:
#   1. <vault>/.devin/skills/<name>/SKILL.md (for the repo plugin and cloud sessions)
#   2. ~/.config/devin/skills/<name>/SKILL.md (when --install-global is passed)
#
# Usage:
#   python3 tools/sync_skills.py                  # update .devin/skills/
#   python3 tools/sync_skills.py --install-global # update .devin/skills/ and ~/.config/devin/skills/
#   python3 tools/sync_skills.py --check          # exit 1 if .devin/skills/ is out of date

import shutil
import sys
from pathlib import Path

SKILL_ALLOWED_TOOLS = {
    "compound-memory": ["read", "edit", "grep", "glob", "exec"],
    "style-linter": ["read", "grep", "glob", "exec"],
    "pr-review-loop": ["read", "grep", "glob", "exec"],
    "adr-writing": ["read", "edit", "grep", "glob"],
    "unslop": ["read", "edit", "grep", "glob"],
    "parallel-agents": ["read", "grep", "glob", "exec"],
    "writing-skills": ["read", "edit", "grep", "glob", "exec"],
}

DEFAULT_ALLOWED_TOOLS = ["read", "grep", "glob"]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end_marker = text.find("\n---\n", 4)
    if end_marker == -1:
        raise ValueError("unclosed YAML frontmatter")

    raw_header = text[4:end_marker]
    body = text[end_marker + 5:]
    fields: dict[str, str] = {}
    for line in raw_header.split("\n"):
        if ":" not in line or line.startswith(" ") or line.startswith("-"):
            continue
        key, raw_value = line.split(":", 1)
        cleaned = raw_value.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
            cleaned = cleaned[1:-1]
        fields[key.strip()] = cleaned
    return fields, body


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return '"' + escaped + '"'


def build_skill_markdown(name: str, description: str, body: str) -> str:
    allowed_tools = SKILL_ALLOWED_TOOLS.get(name, DEFAULT_ALLOWED_TOOLS)
    lines = [
        "---",
        "name: " + name,
        "description: " + yaml_quote(description),
        "triggers:",
        "  - user",
        "  - model",
        "allowed-tools:",
    ]
    for tool_name in allowed_tools:
        lines.append("  - " + tool_name)
    lines.append("---")
    lines.append("")
    trimmed_body = body.lstrip("\n")
    return "\n".join(lines) + trimmed_body


def collect_expected_skills(vault_root: Path) -> dict[str, str]:
    skills_dir = vault_root / "Skills"
    rendered: dict[str, str] = {}
    for note_path in sorted(skills_dir.glob("*.md")):
        text = note_path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text)
        skill_name = fields.get("name", "").strip()
        description = fields.get("description", "").strip()
        if skill_name == "" or description == "":
            raise ValueError(str(note_path) + " must define 'name' and 'description' in frontmatter")
        rendered[skill_name] = build_skill_markdown(skill_name, description, body)
    return rendered


def check_target_dir(target_root: Path, expected: dict[str, str]) -> list[str]:
    problems = []
    existing_dirs = set()
    if target_root.is_dir():
        for child in sorted(target_root.iterdir()):
            if child.is_dir():
                existing_dirs.add(child.name)

    for skill_name, expected_text in expected.items():
        skill_file = target_root / skill_name / "SKILL.md"
        if not skill_file.is_file():
            problems.append("missing exported skill: " + str(skill_file))
            continue
        actual_text = skill_file.read_text(encoding="utf-8")
        if actual_text != expected_text:
            problems.append("out-of-date exported skill: " + str(skill_file))

    for extra_name in sorted(existing_dirs - set(expected.keys())):
        problems.append("stale exported skill folder: " + str(target_root / extra_name))

    return problems


def write_target_dir(target_root: Path, expected: dict[str, str], prune_extra: bool) -> None:
    target_root.mkdir(parents=True, exist_ok=True)
    for skill_name, expected_text in expected.items():
        skill_dir = target_root / skill_name
        if skill_dir.is_symlink():
            skill_dir.unlink()
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        if skill_file.is_file() and skill_file.read_text(encoding="utf-8") == expected_text:
            continue
        skill_file.write_text(expected_text, encoding="utf-8")

    if not prune_extra:
        return
    for child in sorted(target_root.iterdir()):
        if child.is_dir() and child.name not in expected:
            shutil.rmtree(child)


def default_global_skills_dir() -> Path:
    return Path.home() / ".config" / "devin" / "skills"


def sync_skills(vault_root: Path, install_global: bool = False, global_dir: Path | None = None) -> list[str]:
    expected = collect_expected_skills(vault_root)
    repo_skills_dir = vault_root / ".devin" / "skills"
    write_target_dir(repo_skills_dir, expected, prune_extra=True)

    if install_global:
        destination = global_dir if global_dir is not None else default_global_skills_dir()
        write_target_dir(destination, expected, prune_extra=False)

    return sorted(expected.keys())


def main() -> None:
    args = set(sys.argv[1:])
    vault_root = Path(__file__).resolve().parent.parent
    expected = collect_expected_skills(vault_root)
    repo_skills_dir = vault_root / ".devin" / "skills"

    if "--check" in args:
        problems = check_target_dir(repo_skills_dir, expected)
        for problem in problems:
            print(problem)
        if len(problems) > 0:
            sys.exit(1)
        print("Exported skills are in sync (" + str(len(expected)) + " skills).")
        return

    install_global = "--install-global" in args
    names = sync_skills(vault_root, install_global=install_global)
    summary = ", ".join(names)
    print("Synced " + str(len(names)) + " skills: " + summary)


if __name__ == "__main__":
    main()
