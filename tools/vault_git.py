# Git helpers for syncing agent-vault with GitHub. Used by sync_vault.py.

import subprocess
from pathlib import Path

GIT_NETWORK_TIMEOUT_SECONDS = 15
GIT_LOCAL_TIMEOUT_SECONDS = 10

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
