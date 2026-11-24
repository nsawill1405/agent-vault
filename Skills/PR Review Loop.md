---
name: pr-review-loop
description: Use when finishing a change. Verify locally, open a PR, and work through CI and review feedback until it is ready for William.
type: skill
tags:
  - skill
  - workflow
source: "https://github.com/Robbie-Palmer/hq/blob/main/.agents/skills/complete-pr-review-loop/references/review-loop.md"
author: Adapted for William from Robbie Palmer
---

# PR review loop

Adapted from the hq `complete-pr-review-loop` skill. The hq version names SonarQube projects, Doppler configs, and a custom review bot that only exist in that repo. This version keeps the process and drops those details.

Do not merge unless William asks. See [[Workflow Preferences]].

## Before opening the PR

Do not use the PR as the first test run.

1. Sync with the base branch and read the full diff.
2. Match tests to the change. Unit tests for logic, integration tests for boundaries, UI checks only when lower-level tests cannot cover the behavior.
3. Run the repo's linter, formatter, type checker, and tests. Run `tools/style_lint.py` from this vault on the changed files if the repo has no stricter linter. See [[Style Linter]].
4. Fix failures before pushing. If a check cannot run, say why in the PR.

Commit only the intended work. Never add Devin or any AI agent as a `Co-Authored-By` trailer, and never mention Devin, AI agents, session links, or "Generated with" footers in commit messages, PR titles, PR descriptions, or comments. Open the PR with a short summary and the checks you ran, written in William's voice.

## Write PR descriptions from files

Write the description to a Markdown file and pass it with `gh pr create --body-file <path>`.
Inline multi-line shell arguments break backticks and newlines.
After creating the PR, read it back once with `gh pr view` and fix damaged formatting.

## Review cycle

1. Wait a few minutes after each push, then take one snapshot of CI and review comments. Do not poll in a tight loop.
2. Classify each finding as a real issue, a worthwhile nit, stale or duplicate, or a false positive.
3. Fix real issues and add a test that would have caught them.
4. Reply briefly with evidence when rejecting a finding.
5. Batch fixes, rerun local checks, push, and repeat.

Do not churn code just to satisfy a reviewer's preference. Review bots give suggestions, not orders.

## Done means

- CI passes.
- No real review finding is left open.
- Every fix is committed and pushed.
- Reusable lessons, failed approaches, and repo quirks are recorded in `Memory/` through [[Compound Memory]].
- William gets the PR link and one line on anything still outstanding.
