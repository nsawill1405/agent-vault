---
name: compound-memory
description: Read prior lessons before non-trivial work, and compound what worked or failed into agent-vault Memory/ with automatic lint and GitHub sync.
type: skill
tags:
  - skill
  - memory
  - workflow
---

# Compound memory

Use `agent-vault` as a compounding engineering knowledge base across sessions and repositories.
Every non-trivial debugging session, tricky implementation, or failed experiment should leave the next session smarter than the last.

## Vault location

1. On William's Mac, the live Obsidian vault is `/Users/williamnorth/Downloads/agent-vault` and is also exposed through the `obsidian` MCP server as vault `agent-vault`.
2. In a remote or cloud environment without that folder, clone `nsawill1405/agent-vault` with `gh repo clone nsawill1405/agent-vault /tmp/agent-vault` (or pull it if already cloned).

## Step 1. Recall before starting work

Before debugging an unfamiliar failure, designing a feature, or touching an engine boundary (Roblox, Unity, macOS, Python, TypeScript):

1. Check [[Memory Index]] and search `Memory/` for the repo name, runtime, API, or symptom.
2. Read matching notes in `Memory/Project Notes/`, `Memory/Failures and Fixes/`, and `Memory/Patterns/`.
3. Treat `William/` as highest authority, `Memory/` as tested operational lessons, and `Knowledge Graph/` as general background.

## Step 2. Decide whether the session produced durable knowledge

Write or update a vault note when any of these happened:

- An initial approach failed for a non-obvious reason and you found the real root cause.
- A pattern, tool flag, or test setup solved a tricky problem cleanly and will apply again.
- You uncovered a repo-specific invariant, build quirk, or environment constraint worth knowing up front next time.
- William stated a new rule or correction about how he wants code, commits, UI, or workflows handled.

Skip routine work that taught nothing reusable, such as renaming a variable, fixing a typo, or answering a one-off question. Noise weakens retrieval.

## Step 3. Pick the right folder and compound in place

- New stated or observed preferences from William go in `William/`, marked `(stated)` or `(observed)`.
- Reusable implementation approaches go in `Memory/Patterns/`.
- Debugging postmortems, API traps, and dead ends go in `Memory/Failures and Fixes/`.
- Repo-specific architecture and workflow facts go in `Memory/Project Notes/`.
- Cross-repo tool or design tradeoffs go in `Memory/Decisions/`.

Always search `Memory/` before creating a file:

1. If a note already covers the repo or topic, edit that note in place. Merge the new scenario, sharpen when an approach works versus fails, remove wrong assumptions, and update the `updated` date.
2. Only create a new note when the subject is distinct. Check that no other note in the vault already uses the same file name.
3. Add a link to any new note under the matching heading in [[Memory Index]].
4. Connect the note with `[[wikilinks]]` by note name to [[Memory Index]], relevant `William/` notes such as [[Coding Principles]] or [[Workflow Preferences]], and matching `Knowledge Graph/` ideas such as [[Idempotency]] or [[Context Engineering]].
5. Follow [[Unslop]] on every line. Never use em dashes, en dashes, curly quotes, or AI filler words.

## Note format

```markdown
---
title: Clear specific title
type: memory
outcome: worked
updated: "2026-11-24"
tags:
  - memory
  - roblox
---

# Clear specific title

One-sentence takeaway naming the constraint or fix.

## Scenario

Which project, runtime, or subsystem hit this problem, and the exact symptom.

## What failed

What was tried first and the concrete reason it broke. Omit this section when nothing failed.

## What worked

The verified fix, invariant, or pattern, with a short code snippet or command when useful.

## Related

- [[Memory Index]]
```

Allowed `outcome` values are `worked`, `failed`, `mixed`, and `reference`.

## Step 4. Validate and sync to GitHub

On William's Mac, run one command to lint the vault, run style and unit tests, commit as William with no agent attribution, rebase on `origin/main`, and push:

```bash
python3 /Users/williamnorth/Downloads/agent-vault/tools/sync_vault.py push "Record <topic> in memory"
```

In a cloud session with a temporary clone:

```bash
python3 tools/vault_lint.py
python3 tools/style_lint.py tools
python3 -m unittest discover -s tools/tests
git add Memory William Skills Home.md AGENTS.md README.md
git commit -m "Record <topic> in memory"
git pull --rebase origin main
git push origin main
```

Never add Devin or any AI agent as a co-author or mention Devin in the commit message.
