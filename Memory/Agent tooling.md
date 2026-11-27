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
- Devin's PR tool appends a session link footer, and Devin Review re-appends a badge after every push. About 30 seconds after the last push, rewrite the body with `gh pr edit --body-file` and confirm with `gh api repos/<owner>/<repo>/pulls/<n> -q .body`.
- The Devin VM wraps `git commit` in a shell function that always adds a `Co-Authored-By: Devin AI` trailer. Commit with `( source /opt/.devin/git_author; /usr/bin/git commit -m "..." )` and check `git log -1 --format=%B` before pushing.
- `tools/style_lint.py` reports hundreds of existing findings in older repos such as unity-debug-watch. Map `git diff -U0` hunks to finding line numbers and fix only the lines you added.
- The PR tool rehosts local screenshots on app.devin.ai links. For a PR body with no agent links, push the images to a separate orphan branch and embed `https://github.com/<owner>/<repo>/blob/<branch>/<file>?raw=true`.
- Child sessions add `Co-Authored-By: Devin AI` trailers to their own commits, and a GitHub squash merge copies every commit body into the commit on `main`. Tell each child to use the `git_author` workaround, and run `git log --format=%B main..HEAD | grep -i co-authored` before opening the final PR.
- A repo made from Devin's new-repo card already has an "Initial commit" with a README. Fetch and rebase before the first push. In a rebase, `-X ours` keeps the upstream side, not yours.

## Related

- [[Memory Index]]
- [[Parallel Agents]]
