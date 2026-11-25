---
title: Agent tooling
type: memory
updated: "2026-11-25"
tags:
  - memory
  - agents
---

# Agent tooling

Lessons about the agent platforms William uses.

- The Devin GitHub app cannot change repository visibility (HTTP 403). William changes visibility himself.
- The Devin GitHub app cannot push to `nsawill1405/gears-game-jam`, so lessons from that repo stay in this vault.
- Devin's PR tool appends a session link footer, and Devin Review re-appends a badge after every push. About 30 seconds after the last push, rewrite the body with `gh pr edit --body-file` and confirm with `gh api repos/<owner>/<repo>/pulls/<n> -q .body`.
- The Devin VM wraps `git commit` in a shell function that always adds a `Co-Authored-By: Devin AI` trailer. Commit with `( source /opt/.devin/git_author; /usr/bin/git commit -m "..." )` and check `git log -1 --format=%B` before pushing.
- `tools/style_lint.py` reports hundreds of existing findings in older repos such as unity-debug-watch. Map `git diff -U0` hunks to finding line numbers and fix only the lines you added.

## Related

- [[Memory Index]]
- [[Parallel Agents]]
