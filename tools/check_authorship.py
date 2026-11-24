#!/usr/bin/env python3
# Blocks git commits and GitHub PR or release commands that include Devin or AI co-author
# trailers, "Generated with" footers, session URLs, or Devin mentions in titles and bodies.
# Runs as a Devin PreToolUse command hook on exec, reading hook JSON from stdin.

import json
import os
import re
import shlex
import sys
from pathlib import Path

COMMIT_OR_PR_COMMAND = re.compile(
    r"\bgit\b.*\bcommit\b|\bgh\b.*\b(?:pr\s+(?:create|edit|comment)|release\s+create)\b",
    re.DOTALL,
)

FORBIDDEN_COMMAND_PATTERNS = [
    (re.compile(r"co-authored-by\s*:.*(?:devin|claude|cursor|copilot|agent|noreply\.anthropic)", re.IGNORECASE),
     "co-author trailer"),
    (re.compile(r"devin-ai-integration", re.IGNORECASE), "Devin bot identity"),
    (re.compile(r"generated\s+(?:with|by)\s+\[?devin", re.IGNORECASE), "'Generated with Devin' footer"),
    (re.compile(r"https?://(?:app\.)?devin\.ai\b", re.IGNORECASE), "Devin URL"),
]

STANDALONE_DEVIN_WORD = re.compile(r"(?<![./\w-])devin(?![\w-])", re.IGNORECASE)

TEXT_VALUE_FLAGS = {"-m", "--message", "-t", "--title", "-b", "--body"}
FILE_VALUE_FLAGS = {"-F", "--file", "--body-file"}


def check_raw_text_for_trailers(text: str) -> str | None:
    for pattern, label in FORBIDDEN_COMMAND_PATTERNS:
        if pattern.search(text):
            return label
    return None


def check_prose_for_devin_mention(text: str) -> str | None:
    trailer_hit = check_raw_text_for_trailers(text)
    if trailer_hit is not None:
        return trailer_hit
    if STANDALONE_DEVIN_WORD.search(text):
        return "Devin mention in title, message, or description"
    return None


def split_shell_tokens(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def extract_flag_values(tokens: list[str], flags: set[str]) -> list[str]:
    values = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in flags and index + 1 < len(tokens):
            values.append(tokens[index + 1])
            index = index + 2
            continue
        for flag in flags:
            prefix = flag + "="
            if token.startswith(prefix):
                values.append(token[len(prefix):])
        index = index + 1
    return values


def resolve_candidate_file(raw_path: str, base_dir: Path) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate
    return base_dir / candidate


def inspect_message_text(text: str) -> str | None:
    reason = check_prose_for_devin_mention(text)
    if reason is None:
        return None
    return (
        "Blocked by William's authorship rule (" + reason + "). "
        "Never add Devin as a co-author or mention Devin in commit messages, PR titles, "
        "descriptions, or comments. Write everything in William's voice."
    )


def inspect_command(command: str, base_dir: Path | None = None) -> str | None:
    if not COMMIT_OR_PR_COMMAND.search(command):
        return None

    trailer_hit = check_raw_text_for_trailers(command)
    if trailer_hit is not None:
        return (
            "Blocked by William's authorship rule (" + trailer_hit + "). "
            "Remove Co-Authored-By trailers, 'Generated with Devin' lines, and Devin links."
        )

    working_dir = base_dir if base_dir is not None else Path.cwd()
    tokens = split_shell_tokens(command)

    inline_texts = extract_flag_values(tokens, TEXT_VALUE_FLAGS)
    for text in inline_texts:
        violation = inspect_message_text(text)
        if violation is not None:
            return violation

    file_paths = extract_flag_values(tokens, FILE_VALUE_FLAGS)
    for raw_path in file_paths:
        if raw_path == "-":
            continue
        resolved = resolve_candidate_file(raw_path, working_dir)
        if resolved.is_file():
            content = resolved.read_text(encoding="utf-8", errors="replace")
            violation = inspect_message_text(content)
            if violation is not None:
                return violation

    # Catch heredoc commit or PR bodies passed inline via $(cat <<'EOF' ... EOF).
    if "<<" in command:
        violation = inspect_message_text(command)
        if violation is not None:
            return violation

    return None


def main() -> None:
    raw_stdin = sys.stdin.read()
    if raw_stdin.strip() == "":
        return

    try:
        payload = json.loads(raw_stdin)
    except json.JSONDecodeError:
        return

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return

    command = tool_input.get("command")
    if not isinstance(command, str):
        return

    workdir_value = tool_input.get("workdir") or os.environ.get("DEVIN_PROJECT_DIR")
    base_dir = Path(workdir_value) if isinstance(workdir_value, str) and workdir_value else Path.cwd()

    reason = inspect_command(command, base_dir)
    if reason is not None:
        response = {"decision": "block", "reason": reason}
        print(json.dumps(response))


if __name__ == "__main__":
    main()
