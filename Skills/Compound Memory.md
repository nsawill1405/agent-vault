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
3. Open [[Memory Index]], then the hub for the topic, such as [[Unity]] or [[Roblox]]. Read only the notes the hub lists that match the task.

## After work

Record a lesson only if it is tested, likely to matter again, and not obvious from the code. Skip task status, dates, PR numbers and anything cheap to rediscover.

Put it in exactly one place:

| Lesson | Where |
| --- | --- |
| A preference or rule William stated | `William/`, marked "(stated)" |
| A fact about one repo: build commands, invariants, traps in its own code | That repo's `AGENTS.md`, in a PR. Skip it if agents cannot push to the repo |
| A trap or fix that applies in several repos, such as an engine or tool quirk | The matching area note in `Memory/<Topic>/` |
| A repeatable multi-step procedure | A new skill. Follow [[Writing Skills]] |

## How to write it

- One bullet per rule, one or two sentences. Lead with the rule, then the reason. Include the exact API, command or error text.
- Edit an existing bullet if it is wrong or partly covered. Delete bullets that are no longer true.
- Keep each note to one area, so agents read only what they need. When a note covers two areas or passes about 15 bullets, split it.
- New area in an existing topic: add `Memory/<Topic>/<Area>.md`, link it from the topic hub with a short description, and link the hub from its `## Related` section.
- New topic: create `Memory/<Topic>/<Topic>.md` as a hub with `type: index`, and add it to [[Memory Index]]. A topic with only a few rules can stay a single note in `Memory/` until it grows.
- Every note needs `type` and `tags` in frontmatter and a `## Related` section. Link related notes in other topics too, so the graph shows the connection.
- Note names must be unique across the vault. Prefix area notes with the topic, such as `Unity API traps`.
- Never record secrets, tokens, or private data from other people. Use `~` instead of full home paths.
- Follow [[Unslop]].

## Sync

`Memory/`, `William/` and `Skills/` changes go straight to `main` so every session sees them. Run this from the vault root, with the vault on `main`:

```bash
cd <vault> && python3 tools/sync_vault.py push "Record <topic> in memory"
```

The command runs the vault linter and skill export check, commits only vault notes, pulls with rebase and pushes. The Devin plugin hook also runs it at session end.
