---
title: hq Overview
type: reference
tags:
  - hq
  - reference
---

# hq overview

[hq](https://github.com/nsawill1405/hq) is William's fork of [Robbie Palmer's hq](https://github.com/Robbie-Palmer/hq).
It is a Next.js site backed by a typed content graph of projects, ADRs, PDRs, ideas, initiatives, roles, and technologies.
The notes in `Knowledge Graph/` are the agent-related part of that graph. See [[Knowledge Graph Index]].

## How the graph maps to Obsidian

hq builds the graph in `ui/lib/repository/graph/` and serves it at `/knowledge-graph.json`.
Entities come from MDX frontmatter. The importer turns those relationships into wikilinks.

| hq edge | Vault equivalent |
| --- | --- |
| `REFERENCES_IDEA`, `RELATED_IDEA`, `HAS_IDEA` | Links in the note body and `## Links` |
| `CONTRIBUTES_TO_INITIATIVE` | `initiatives:` entries in `## Links` |
| `PART_OF_PROJECT` | `project:` entry in `## Links`, and the project folder |
| `SUPERSEDES` | `supersedes:` entry in `## Links` |
| `USES_TECHNOLOGY` | `tech_stack` frontmatter list |

Links to hq pages that were not imported point at robbiepalmer.me instead.

## What was imported

- All idea pages. They explain general concepts like idempotency, human-on-the-loop, and context engineering.
- The Semi-Autonomous Software Development initiative.
- Five agentic projects with their ADRs and PDRs: Agent Coordinator, Agent-First Writing, Agent-Friendly Remote Development, Agentic Code Review, and Work Graph.
- Agent tooling ADRs from the Personal Knowledge Graph project, such as Claude Code, Codex, CodeRabbit, and the content graph.
- The Basic Memory and SilverBullet knowledge base decisions from the homelab project.
- The Building Philosophy page and the AI platform teams blog post.
- Agent runbooks and docs, in `Reference/hq docs/`.

## Rules from hq worth borrowing

These come from hq's `AGENTS.md`. They are Robbie's rules, kept here as useful defaults.

- Run tasks through the repo's task runner, not raw package manager scripts.
- Keep declarative config declarative. Put long shell or Python bodies in checked-in scripts, not in CI YAML or task files.
- Migration names must state an action and a subject, like `add_recipe_notes`.
- Never read, print, or search for credential values. Use only the documented access path.
- An ADR records one choice and only links backward in time. See [[ADR Writing]].
- Agents may not infer permission to merge, deploy, or release. See [[Work Graph Skill]].

## Agent memory in hq

hq runs [Basic Memory](https://github.com/basicmachines-co/basic-memory) on a Mac mini with a `knowledge` project exposed over MCP to Claude Code, Codex, and opencode.
This vault can be registered the same way. See the README.
