---
title: Workflow Preferences
type: profile
tags:
  - william
  - workflow
---

# Workflow Preferences

Part of [[William North]].

## How William works with agents (observed)

- He asks for features one at a time and expects each to be finished and working.
- He often follows a feature with "merge it" or "release it". Do not merge or release before he says so.
- He cares about the end result in the real tool. Test in the actual app, Studio, or editor when possible.
- He likes to be told what changed in one or two lines, not a long report.

## Before calling work done

1. Run the repo's linter, formatter, type checker, and tests.
2. Check the feature by hand in the real environment if it has a UI.
3. Update the README if behavior or setup changed.
4. Update the CHANGELOG if the repo has one.

## Going public or releasing (observed)

When a repo is being prepared for release or open source:

- Run a security pass. Look for committed secrets, tokens, and personal paths.
- Add or refresh the README with a clear pitch, a demo GIF or screenshot, install steps, and usage.
- Add a LICENSE, CI, and issue templates if missing.
- Tag a version and write release notes that list user-visible changes.

## README style (observed)

His profile README and project READMEs use capsule-render headers and footers, shields.io badges,
a featured-projects section, and a "Made by William North · nsawill.co.uk" footer.
Match this style when writing READMEs for his projects.

## Git

- Small, focused commits with plain messages.
- Pull requests by default. Do not push to `main` unless asked. Exception: `Memory/` updates in `agent-vault` push directly to `main` through `tools/sync_vault.py` so the vault stays current across sessions (stated).
- Never rewrite shared history.

## Authorship and attribution (stated)

- Never add Devin or any AI agent as a `Co-Authored-By` trailer on commits or pull requests.
- Never mention Devin, AI agents, session links, badges, or "Generated with" footers in commit messages, PR titles, PR descriptions, code comments, or documentation.
- Write every commit message, PR title, PR description, and comment in William's voice so it reads as written directly by him. Use William's git identity.

## Decision records

For larger architecture choices, write a short ADR. See [[ADR Writing]].
