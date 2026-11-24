# Instructions for coding agents

This repo is an Obsidian vault that describes how William North wants agents to work.
It is meant to be read by agents working in his other repos.

## Using the vault from another repo

1. Read `William/William North.md` and the notes it links to.
2. Check `Memory/Memory Index.md` and search `Memory/` before debugging or planning non-trivial work so you reuse proven fixes and skip known dead ends.
3. Apply `William/Coding Principles.md` to every code change, and run `Skills/Style Linter.md` (`tools/style_lint.py`) on changed code.
4. Apply `Skills/Unslop.md` to READMEs, docs, commit messages, PR text, vault notes, and UI copy.
5. Follow `Skills/PR Review Loop.md` when finishing work.
6. Follow `Skills/Compound Memory.md` after non-trivial tasks to record what worked, what failed, and repo quirks in `Memory/`, then sync with `python3 tools/sync_vault.py push "<summary>"`.
7. Search `Knowledge Graph/` when you need background on agent workflows, decision records, or an idea such as idempotency or human-on-the-loop review.

Notes in `William/` override everything else in this vault. Notes in `Memory/` capture tested lessons from William's projects. Notes in `Knowledge Graph/` and `Reference/` were written by Robbie Palmer for his own hq repo. Treat them as reference material, not as William's rules.

## Authorship rule

Never add Devin or any AI agent as a `Co-Authored-By` trailer on commits or pull requests. Never mention Devin, AI agents, session URLs, or "Generated with" lines in commit messages, PR titles, PR descriptions, code comments, or documentation. Write all commits, PRs, and comments so they read as William's own work.

## Editing the vault

- Use Obsidian `[[wikilinks]]` between notes. Link by note name, not path.
- Every note needs YAML frontmatter with `type` and `tags`.
- Do not hand-edit `Knowledge Graph/` or `Reference/hq docs/`. Re-run the importer instead:
  `python3 tools/import_hq.py <path to hq checkout>`
- Put new facts about William in `William/`. Mark each as stated (William said it) or observed (inferred from his repos).
- Put technical lessons, debugging postmortems, working patterns, and per-repo notes in `Memory/`, following `Skills/Compound Memory.md`. Update existing notes instead of creating duplicates.

## Checks

Run before committing. All three run in CI and in the pre-commit hook.

```bash
python3 tools/vault_lint.py
python3 tools/style_lint.py tools
python3 -m unittest discover -s tools/tests
```

The tools use only the Python standard library. Python 3.10 or newer.
