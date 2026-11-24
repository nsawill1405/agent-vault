# agent-vault

An Obsidian vault of agent skills, a knowledge graph, and William North's working style, for coding agents to read.

## What is in it

- `William/`: how William codes, writes, and ships. Agents should follow these notes.
- `Skills/`: procedures for prose cleanup, ADRs, and the PR review loop.
- `Knowledge Graph/`: 134 notes imported from [hq](https://github.com/nsawill1405/hq): ideas, agentic projects, ADRs, PDRs, and the building philosophy, linked with wikilinks so Obsidian's graph view shows the relationships.
- `Reference/`: background on hq, its Work Graph skill, and its agent docs.
- `tools/`: the hq importer, the vault linter, and a code style linter.

Open the folder in Obsidian and start at `Home.md`.

## Pointing agents at it

Clone the vault next to your other repos, then add a line like this to a repo's `AGENTS.md` or `CLAUDE.md`:

```text
Before working, read ../agent-vault/AGENTS.md and follow ../agent-vault/William/.
```

The vault also works as a [Basic Memory](https://github.com/basicmachines-co/basic-memory) project, which is how hq exposes notes to agents over MCP:

```bash
bm project add agent-vault ~/repos/agent-vault
bm mcp --project agent-vault
```

## Style linter

`tools/style_lint.py` flags code that is hard to explain or debug: nested ternaries, nested comprehensions, long method chains, swallowed errors, and overlong lines. It reads Python, TypeScript, JavaScript, C#, and Luau.

```bash
python3 tools/style_lint.py path/to/repo/src
```

Silence a single line with a `style-lint: ignore` comment that says why. See `Skills/Style Linter.md`.

## Updating from hq

```bash
python3 tools/import_hq.py ../hq
python3 tools/vault_lint.py
```

The importer rewrites `Knowledge Graph/` and `Reference/hq docs/` from scratch. Hand-written notes live elsewhere and are never touched.

## Credit

Content under `Knowledge Graph/`, `Reference/`, `Skills/Unslop.md`, and `Skills/ADR Writing.md` comes from [Robbie Palmer's hq](https://github.com/Robbie-Palmer/hq). Each imported note links to its source.
