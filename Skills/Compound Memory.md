---
name: compound-memory
description: Use before non-trivial debugging or planning to load past lessons, and after finishing a task to record what worked, what failed, and repo quirks as short rules in the right place.
type: skill
tags:
  - skill
  - memory
  - workflow
---

# Compound memory

This vault is the single knowledge base for William's agents. Every lesson goes in one place, as a short rule, so the next session reads it instead of rediscovering it. Do not store lessons in an agent's private memory.

## Find the vault

1. On William's Mac it is `~/Downloads/agent-vault`, also exposed through the `obsidian` MCP server as vault `agent-vault`.
2. In a cloud session, use the checkout in the repos folder, or run `gh repo clone nsawill1405/agent-vault ../agent-vault` and `git -C ../agent-vault pull`.

## Before work

1. Read [[William North]]. It is short and overrides everything else.
2. Read the current repo's `AGENTS.md`.
3. Open [[Memory Index]] and read the topic notes that match the task, such as [[Unity]] or [[Roblox]]. If the repo has a note in `Memory/Projects/`, read it too.

## After work

Record a lesson only if it is tested, likely to matter again, and not obvious from the code. Skip task status, dates, PR numbers and anything cheap to rediscover.

Put it in exactly one place:

| Lesson | Where |
| --- | --- |
| A preference or rule William stated | `William/`, marked "(stated)" |
| A fact about one repo: build commands, invariants, traps in its own code | That repo's `AGENTS.md`, in a PR |
| A trap or fix that applies in several repos, such as an engine or tool quirk | The matching topic note in `Memory/` |
| A fact about a repo agents cannot push to | `Memory/Projects/<repo>.md` |
| A repeatable multi-step procedure | A new skill. Follow [[Writing Skills]] |

## How to write it

- One bullet per rule, one or two sentences. Lead with the rule, then the reason. Include the exact API, command or error text.
- Edit an existing bullet if it is wrong or partly covered. Delete bullets that are no longer true.
- Create a topic note only when no existing note fits. Give it `type: memory` and `tags` in frontmatter, a `## Related` section linking [[Memory Index]], and add it to [[Memory Index]].
- Never record secrets, tokens, or private data from other people. Use `~` instead of full home paths.
- Follow [[Unslop]].

## Sync

`Memory/`, `William/` and `Skills/` changes go straight to `main` so every session sees them. Run this from the vault root, with the vault on `main`:

```bash
cd <vault> && python3 tools/sync_vault.py push "Record <topic> in memory"
```

The command runs the vault linter and skill export check, commits only vault notes, pulls with rebase and pushes. The Devin plugin hook also runs it at session end.
