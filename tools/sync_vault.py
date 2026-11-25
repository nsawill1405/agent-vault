#!/usr/bin/env python3
# Validates, commits, and syncs agent-vault with GitHub, and handles Devin session hooks.
#
# Usage:
#   python3 tools/sync_vault.py pull
#   python3 tools/sync_vault.py push [commit message]
#   python3 tools/sync_vault.py session-start
#   python3 tools/sync_vault.py session-end

import io
import json
import subprocess
import sys
import unittest
from pathlib import Path

import check_authorship
import style_lint
import sync_skills
import vault_lint

GIT_NETWORK_TIMEOUT_SECONDS = 15
GIT_LOCAL_TIMEOUT_SECONDS = 10
RECENT_MEMORY_LIMIT = 5

MANAGED_VAULT_PATHS = [
    "Memory",
    "William",
    "Skills",
    "tools",
    ".devin",
    ".devin-plugin",
    ".github",
    ".gitignore",
    ".pre-commit-config.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "Home.md",
    "README.md",
    "hooks.json",
]

AUTO_SYNC_FOLDERS = ("Memory/", "William/", "Skills/")


def run_git(
    vault_root: Path,
    args: list[str],
    timeout_seconds: int = GIT_LOCAL_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(vault_root),
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )


def should_install_global_skills() -> bool:
    devin_config_dir = Path.home() / ".config" / "devin"
    return devin_config_dir.is_dir()


def validate_vault(vault_root: Path) -> list[str]:
    errors = []
    for finding in vault_lint.lint_vault(vault_root):
        errors.append(str(finding))

    tools_dir = vault_root / "tools"
    for python_file in style_lint.collect_files([str(tools_dir)]):
        for finding in style_lint.lint_file(python_file):
            errors.append(str(finding))

    tests_dir = tools_dir / "tests"
    suite = unittest.defaultTestLoader.discover(start_dir=str(tests_dir))
    output_buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=output_buffer)
    result = runner.run(suite)
    if not result.wasSuccessful():
        errors.append("tools unit tests failed:\n" + output_buffer.getvalue())

    return errors


def pull_vault(vault_root: Path, quiet_network_errors: bool = False) -> bool:
    fetch_result = run_git(vault_root, ["fetch", "origin", "main"], timeout_seconds=GIT_NETWORK_TIMEOUT_SECONDS)
    if fetch_result.returncode != 0:
        if not quiet_network_errors:
            sys.stderr.write("git fetch failed: " + fetch_result.stderr.strip() + "\n")
        return False

    behind_result = run_git(vault_root, ["rev-list", "--count", "HEAD..origin/main"])
    if behind_result.returncode != 0:
        return False

    behind_count = int(behind_result.stdout.strip() or "0")
    if behind_count == 0:
        return True

    rebase_result = run_git(
        vault_root,
        ["pull", "--rebase", "--autostash", "origin", "main"],
        timeout_seconds=GIT_NETWORK_TIMEOUT_SECONDS,
    )
    if rebase_result.returncode != 0:
        if not quiet_network_errors:
            sys.stderr.write("git pull --rebase failed: " + rebase_result.stderr.strip() + "\n")
        return False

    sync_skills.sync_skills(vault_root, install_global=should_install_global_skills())
    return True


def stage_managed_paths(vault_root: Path) -> None:
    existing = []
    for relative_path in MANAGED_VAULT_PATHS:
        candidate = vault_root / relative_path
        if candidate.exists():
            existing.append(relative_path)
    if len(existing) > 0:
        run_git(vault_root, ["add", "--", *existing])


def has_staged_changes(vault_root: Path) -> bool:
    diff_result = run_git(vault_root, ["diff", "--cached", "--quiet"])
    return diff_result.returncode != 0


def ahead_of_origin_count(vault_root: Path) -> int:
    ahead_result = run_git(vault_root, ["rev-list", "--count", "origin/main..HEAD"])
    if ahead_result.returncode != 0:
        return 0
    return int(ahead_result.stdout.strip() or "0")


def current_branch(vault_root: Path) -> str:
    branch_result = run_git(vault_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    return branch_result.stdout.strip()


def push_vault(vault_root: Path, message: str) -> int:
    branch = current_branch(vault_root)
    if branch != "main":
        sys.stderr.write("Vault is on branch '" + branch + "'. Switch to main before syncing, or open a PR instead.\n")
        return 1

    authorship_error = check_authorship.inspect_message_text(message)
    if authorship_error is not None:
        sys.stderr.write(authorship_error + "\n")
        return 1

    sync_skills.sync_skills(vault_root, install_global=should_install_global_skills())
    validation_errors = validate_vault(vault_root)
    if len(validation_errors) > 0:
        for error in validation_errors:
            sys.stderr.write(error + "\n")
        return 1

    stage_managed_paths(vault_root)
    if has_staged_changes(vault_root):
        commit_result = run_git(vault_root, ["commit", "-m", message])
        if commit_result.returncode != 0:
            sys.stderr.write("git commit failed: " + commit_result.stderr.strip() + "\n")
            return 1

    if ahead_of_origin_count(vault_root) == 0:
        print("Vault is clean and already synced with origin/main.")
        return 0

    if not pull_vault(vault_root, quiet_network_errors=False):
        return 1

    push_result = run_git(vault_root, ["push", "origin", "main"], timeout_seconds=GIT_NETWORK_TIMEOUT_SECONDS)
    if push_result.returncode != 0:
        sys.stderr.write("git push failed: " + push_result.stderr.strip() + "\n")
        return 1

    print("Synced vault changes to origin/main.")
    return 0


def list_recent_memory_notes(vault_root: Path) -> list[str]:
    memory_dir = vault_root / "Memory"
    if not memory_dir.is_dir():
        return []

    candidates = []
    for path in memory_dir.rglob("*.md"):
        if path.name == "Memory Index.md":
            continue
        stat = path.stat()
        candidates.append((stat.st_mtime, path.stem))

    candidates.sort(reverse=True)
    titles = []
    for _, stem in candidates[:RECENT_MEMORY_LIMIT]:
        titles.append(stem)
    return titles


def build_session_context(vault_root: Path) -> str:
    memory_dir = vault_root / "Memory"
    note_count = 0
    if memory_dir.is_dir():
        for path in memory_dir.rglob("*.md"):
            if path.name != "Memory Index.md":
                note_count = note_count + 1

    recent_titles = list_recent_memory_notes(vault_root)
    summary = "agent-vault synced at " + str(vault_root) + " (" + str(note_count) + " memory note(s))."
    if len(recent_titles) > 0:
        summary = summary + " Recent memory notes: " + ", ".join(recent_titles) + "."
    summary = (
        summary
        + " This vault is the single knowledge base: read William/William North.md first, check Memory/Memory Index.md "
        + "before non-trivial work, split independent work across parallel subagents with /parallel-agents, "
        + "record lessons with /compound-memory, and write reusable procedures as skills with /writing-skills. "
        + "Never add Devin co-author trailers or mention Devin in commits, PRs, or comments."
    )
    return summary


def handle_session_start(vault_root: Path) -> int:
    try:
        pull_vault(vault_root, quiet_network_errors=True)
    except subprocess.TimeoutExpired as error:
        sys.stderr.write("agent-vault pull timed out during session-start: " + str(error) + "\n")

    sync_skills.sync_skills(vault_root, install_global=should_install_global_skills())
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": build_session_context(vault_root),
        }
    }
    print(json.dumps(payload))
    return 0


def has_dirty_auto_sync_files(vault_root: Path) -> bool:
    status_result = run_git(vault_root, ["status", "--porcelain"])
    if status_result.returncode != 0:
        return False
    for raw_line in status_result.stdout.splitlines():
        if len(raw_line) < 4:
            continue
        file_part = raw_line[3:].strip().strip('"')
        for prefix in AUTO_SYNC_FOLDERS:
            if file_part.startswith(prefix):
                return True
    return False


def handle_session_end(vault_root: Path) -> int:
    if not has_dirty_auto_sync_files(vault_root) and ahead_of_origin_count(vault_root) == 0:
        return 0

    try:
        sync_skills.sync_skills(vault_root, install_global=should_install_global_skills())
        if len(validate_vault(vault_root)) > 0:
            return 0
        stage_managed_paths(vault_root)
        if has_staged_changes(vault_root):
            run_git(vault_root, ["commit", "-m", "Update vault memory notes"])
        if ahead_of_origin_count(vault_root) > 0:
            pull_vault(vault_root, quiet_network_errors=True)
            run_git(vault_root, ["push", "origin", "main"], timeout_seconds=GIT_NETWORK_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        return 0

    return 0


def main() -> None:
    vault_root = Path(__file__).resolve().parent.parent
    command = sys.argv[1] if len(sys.argv) > 1 else "pull"

    if command == "pull":
        ok = pull_vault(vault_root, quiet_network_errors=False)
        sys.exit(0 if ok else 1)

    if command == "push":
        message = " ".join(sys.argv[2:]).strip()
        if message == "":
            message = "Update vault memory notes"
        sys.exit(push_vault(vault_root, message))

    if command == "session-start":
        sys.exit(handle_session_start(vault_root))

    if command == "session-end":
        sys.exit(handle_session_end(vault_root))

    sys.stderr.write("Unknown command: " + command + "\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
