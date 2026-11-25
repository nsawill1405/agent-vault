---
title: Workflow Preferences
type: profile
tags:
  - william
  - workflow
---

# Workflow Preferences

Part of [[William North]].

## Working with agents

- Split tasks into independent parts and run them in parallel subagents. Give subagents distinct roles such as explorer, implementer, reviewer and tester. William said: "split up tasks and work in parallel, and branch out into different roles" and "split into subagents to work in parallel to get code written quickly." See [[Parallel Agents]] (stated).
- When a procedure will come up again, write it as a skill so later sessions load it automatically. See [[Writing Skills]] (stated).
- Use this vault as the knowledge base. Do not keep preferences or lessons in an agent's private memory. Put them in `William/`, `Memory/`, or the repo's `AGENTS.md` (stated).
- He asks for features one at a time and expects each to be finished and working (observed).
- Do not merge or release before he says "merge it" or "release it" (observed).
- Test in the real app, Studio or editor when possible (observed).
- Report what changed in one or two lines, not a long report (observed).

## Before calling work done

1. Run the repo's linter, formatter, type checker and tests.
2. Check the feature by hand in the real environment if it has a UI.
3. Update the README if behavior or setup changed, and the CHANGELOG if the repo has one.

## Going public or releasing (observed)

- Run a security pass for secrets, tokens, personal paths, and notes about private repos.
- Add a README with a pitch, a demo GIF or screenshot, install steps and usage. Add a LICENSE, CI and issue templates if missing.
- Tag a version and write release notes that list user-visible changes.

## README style (stated)

Match his profile README (`nsawill1405/nsawill1405`): capsule-render header and footer, for-the-badge shields, and a "Made by William North · nsawill.co.uk" footer.
Embed demo clips as committed GIFs, not `.mp4` links. Put a hero GIF under the tagline and give each other clip its own section.

## Git

- Small, focused commits with plain messages.
- Pull requests by default. Do not push to `main` unless asked. Exception: `Memory/`, `William/` and `Skills/` changes in `agent-vault` go straight to `main` through `tools/sync_vault.py` so every session sees them (stated).
- Never rewrite shared history.

## Authorship and attribution (stated)

- Never add Devin or any AI agent as a `Co-Authored-By` trailer.
- Never mention Devin, AI agents, session links, "Requested by", badges, or "Generated with" footers in commit messages, PR titles, PR descriptions, code comments or docs. Strip any footer a tool appends right after creating or updating a PR.
- Write commits, PRs and comments in William's voice. Use William's git identity.

## Local inference (stated)

Prefer MLX over `llama.cpp` on Apple Silicon.
