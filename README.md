# agent-vault

A private Obsidian vault that is the single knowledge base for William North's coding agents: his rules, cross-project lessons, and skills that load automatically.

## What is in it

- `William/`: how William codes, writes, and ships. Short, and overrides everything else.
- `Memory/`: one topic note per area (Unity, Roblox, local inference, agent tooling), each a list of short tested rules. Facts about a single repo live in that repo's `AGENTS.md` instead.
- `Skills/`: procedures for parallel subagents, writing new skills, compounding memory, prose cleanup, ADRs, style checks, and the PR review loop. Each one is exported to `.devin/skills/`.
- `tools/`: vault linter, code style linter, authorship check, skill exporter, and GitHub vault sync.

Open the folder in Obsidian and start at `Home.md`.

## How agents use it

The vault is a Devin plugin (`.devin-plugin/plugin.json`). At session start the hook pulls the vault, exports skills, and tells the agent where the rules are. At session end it commits and pushes changes in `Memory/`, `William/` and `Skills/`.

For other agents, add this to a repo's `AGENTS.md` or `CLAUDE.md`:

```text
Before working, read ../agent-vault/AGENTS.md and follow ../agent-vault/William/.
```

## Adding a skill

Write `Skills/<Title>.md` with `name` and `description` frontmatter, then run:

```bash
python3 tools/sync_skills.py
```

See `Skills/Writing Skills.md`. Agents may add skills on their own.

## Style linter

`tools/style_lint.py` flags code that is hard to explain or debug: nested ternaries, nested comprehensions, long method chains, swallowed errors, and overlong lines. It reads Python, TypeScript, JavaScript, C#, and Luau.

```bash
python3 tools/style_lint.py path/to/repo/src
```

Silence a single line with a `style-lint: ignore` comment that says why. See `Skills/Style Linter.md`.

## Credit

`Skills/Unslop.md`, `Skills/ADR Writing.md` and `Skills/PR Review Loop.md` are adapted from [Robbie Palmer's hq](https://github.com/Robbie-Palmer/hq). Each links to its source.
