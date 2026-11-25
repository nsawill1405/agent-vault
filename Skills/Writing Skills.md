---
name: writing-skills
description: Use when you notice a procedure that will come up again, or William asks for a repeatable workflow. Write it as a vault skill so every later session loads it automatically.
type: skill
tags:
  - skill
  - workflow
  - agents
---

# Writing skills

Agents may add their own skills to this vault when they judge one is worth having (stated by William). See [[Workflow Preferences]].

## When to write one

- You followed the same multi-step procedure twice, or expect to.
- A task needed setup or ordering that is easy to get wrong.
- William described a workflow he wants repeated.

Do not write a skill for a single fact. Put facts in `Memory/` or the repo's `AGENTS.md` through [[Compound Memory]]. Before writing, check `Skills/` for an existing skill to extend instead.

## How skills load

`tools/sync_skills.py` exports every `Skills/*.md` note to `.devin/skills/<name>/SKILL.md`. The vault is a Devin plugin (`.devin-plugin/plugin.json`), so every session with the vault checked out loads those skills. On William's Mac, `--install-global` also copies them to `~/.config/devin/skills/`.

## Steps

1. Create `Skills/<Title>.md` with this frontmatter:

   ```markdown
   ---
   name: lower-kebab-name
   description: Use when <trigger>. <What it does in one sentence>.
   type: skill
   tags:
     - skill
   ---
   ```

   Start the description with when to use it. That line decides whether an agent picks the skill.
2. Write the body as numbered steps with exact commands. Keep it under about 100 lines. Follow [[Unslop]].
3. If the skill needs to run or edit files, add its name to `SKILL_ALLOWED_TOOLS` in `tools/sync_skills.py`.
4. Link it from [[Home]].
5. Sync and push. This checks, exports and pushes to `main`:

   ```bash
   python3 tools/sync_vault.py push "Add <name> skill"
   ```

   In a cloud session without push rights to `main`, open a PR instead.
