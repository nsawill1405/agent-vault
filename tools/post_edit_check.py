#!/usr/bin/env python3
# Runs style_lint on edited code files and Unslop prose checks on edited Markdown files.
# Configured as a Devin PostToolUse hook on edit and write so checks fire automatically.

import json
import sys
from pathlib import Path

import style_lint
import vault_lint

SKIPPED_MARKDOWN_PARTS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "Library",
    "Packages",
    ".obsidian",
    ".trash",
    ".devin",
}

IMPORTED_VAULT_PREFIXES = (
    "Knowledge Graph/",
    "Reference/hq docs/",
    "Skills/Unslop.md",
    "Skills/ADR Writing.md",
)

MARKDOWN_SUFFIXES = {".md", ".mdx"}


def find_vault_root_for(file_path: Path) -> Path | None:
    for parent in file_path.parents:
        marker = parent / "tools" / "vault_lint.py"
        if marker.is_file():
            return parent
    return None


def should_skip_markdown(file_path: Path, vault_root: Path | None) -> bool:
    if any(part in SKIPPED_MARKDOWN_PARTS for part in file_path.parts):
        return True
    if vault_root is None:
        return False
    relative_posix = file_path.relative_to(vault_root).as_posix()
    for prefix in IMPORTED_VAULT_PREFIXES:
        if relative_posix.startswith(prefix):
            return True
    return False


def check_edited_file(file_path: Path) -> list[str]:
    if not file_path.is_file():
        return []

    suffix = file_path.suffix.lower()
    findings = []

    is_code_file = (
        suffix in style_lint.PYTHON_SUFFIXES
        or suffix in style_lint.C_STYLE_SUFFIXES
        or suffix in style_lint.LUAU_SUFFIXES
    )
    if is_code_file:
        if any(part in style_lint.SKIPPED_FOLDERS for part in file_path.parts):
            return []
        for item in style_lint.lint_file(file_path):
            findings.append(str(item))
        return findings

    if suffix not in MARKDOWN_SUFFIXES:
        return []

    vault_root = find_vault_root_for(file_path)
    if should_skip_markdown(file_path, vault_root):
        return []

    text = file_path.read_text(encoding="utf-8", errors="replace")
    display_path = file_path.relative_to(vault_root) if vault_root is not None else file_path

    if vault_root is not None and suffix == ".md":
        for item in vault_lint.check_file_name(display_path):
            findings.append(str(item))
        for item in vault_lint.check_frontmatter(display_path, text):
            findings.append(str(item))

    code_free_lines = vault_lint.strip_code(text)
    for item in vault_lint.check_prose(display_path, code_free_lines):
        findings.append(str(item))

    return findings


def build_hook_output(file_path: Path, findings: list[str]) -> dict[str, object]:
    joined = "\n".join(findings)
    message = (
        "Automatic style/Unslop check found issue(s) in "
        + str(file_path)
        + ". Fix these before finishing:\n"
        + joined
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        }
    }


def main() -> None:
    raw_stdin = sys.stdin.read()
    if raw_stdin.strip() == "":
        return

    try:
        payload = json.loads(raw_stdin)
    except json.JSONDecodeError:
        return

    tool_response = payload.get("tool_response")
    if isinstance(tool_response, dict) and tool_response.get("success") is False:
        return

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return

    raw_path = tool_input.get("file_path")
    if not isinstance(raw_path, str) or raw_path.strip() == "":
        return

    resolved_path = Path(raw_path).expanduser()
    findings = check_edited_file(resolved_path)
    if len(findings) == 0:
        return

    print(json.dumps(build_hook_output(resolved_path, findings)))


if __name__ == "__main__":
    main()
