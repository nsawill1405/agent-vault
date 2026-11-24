# Instructions for coding agents

This repo is an Obsidian vault that describes how William North wants agents to work.
It is meant to be read by agents working in his other repos.

## Using the vault from another repo

1. Read `William/William North.md` and the notes it links to.
2. Apply `William/Coding Principles.md` to every code change.
3. Apply `Skills/Unslop.md` to READMEs, docs, commit messages, and UI copy.
4. Follow `Skills/PR Review Loop.md` when finishing work.
5. Search `Knowledge Graph/` when you need background on agent workflows, decision records, or an idea such as idempotency or human-on-the-loop review.

Notes in `William/` override everything else in this vault. Notes in `Knowledge Graph/` and `Reference/` were written by Robbie Palmer for his own hq repo. Treat them as reference material, not as William's rules.

## Editing the vault

- Use Obsidian `[[wikilinks]]` between notes. Link by note name, not path.
- Every note needs YAML frontmatter with `type` and `tags`.
- Do not hand-edit `Knowledge Graph/` or `Reference/hq docs/`. Re-run the importer instead:
  `python3 tools/import_hq.py <path to hq checkout>`
- Put new facts about William in `William/`. Mark each as stated (William said it) or observed (inferred from his repos).

## Checks

Run before committing. All three run in CI and in the pre-commit hook.

```bash
python3 tools/vault_lint.py
python3 tools/style_lint.py tools
python3 -m unittest discover -s tools/tests
```

The tools use only the Python standard library. Python 3.10 or newer.
