# Instructions for coding agents

This repo is an Obsidian vault and the single knowledge base for William North's agents. Agents working in his other repos read it, and write lessons back to it.

## Using the vault from another repo

1. Read `William/William North.md`. It is short, and notes in `William/` override everything else.
2. Read the repo's own `AGENTS.md`, then check `Memory/Memory Index.md` for topic notes that match the task.
3. Split work with more than one independent part across parallel subagents with distinct roles. Follow `Skills/Parallel Agents.md`.
4. Apply `William/Coding Principles.md` to every code change, and run `Skills/Style Linter.md` (`tools/style_lint.py`) on changed code.
5. Apply `Skills/Unslop.md` to READMEs, docs, commit messages, PR text, vault notes, and UI copy.
6. Follow `Skills/PR Review Loop.md` when finishing work.
7. After non-trivial work, record lessons with `Skills/Compound Memory.md`. Write a new skill with `Skills/Writing Skills.md` when a procedure is worth repeating.

Do not keep William's preferences or lessons in an agent's private memory. They belong in this vault or in the repo's `AGENTS.md`.

## Authorship rule

Never add Devin or any AI agent as a `Co-Authored-By` trailer on commits or pull requests. Never mention Devin, AI agents, session URLs, or "Generated with" lines in commit messages, PR titles, PR descriptions, code comments, or documentation. Write all commits, PRs, and comments so they read as William's own work.

## Editing the vault

- Treat the vault as public. Never write secrets, tokens, email addresses, or full home paths (use `~`). `tools/vault_lint.py` blocks them, and the sync refuses to push while it fails.
- Use Obsidian `[[wikilinks]]` between notes. Link by note name, not path.
- Every note needs YAML frontmatter with `type` and `tags`.
- Put facts about William in `William/`. Mark each as stated (William said it) or observed (inferred from his repos).
- Put cross-project lessons in the topic notes in `Memory/` as one-line rules. Put facts about a single repo in that repo's `AGENTS.md`.
- Every `Skills/*.md` note is exported to `.devin/skills/` by `python3 tools/sync_skills.py`. Commit both.

## Checks

Run before committing. They run in CI and in the pre-commit hook.

```bash
python3 tools/vault_lint.py
python3 tools/sync_skills.py --check
python3 tools/style_lint.py tools
python3 -m unittest discover -s tools/tests
```

The tools use only the Python standard library. Python 3.10 or newer.
