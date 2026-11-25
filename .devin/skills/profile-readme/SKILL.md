---
name: profile-readme
description: "Use after creating, deleting, renaming, archiving, publishing or making private one of William's repos, or after a notable change to a featured project. Updates his GitHub profile README so it matches his repos."
triggers:
  - user
  - model
allowed-tools:
  - read
  - edit
  - grep
  - glob
  - exec
---
# Profile README

William's GitHub profile README lives in `nsawill1405/nsawill1405` as `README.md`. William wants it kept up to date automatically, without being asked each time (stated). See [[Projects and Interests]].

## When to update it

- A new public repo is ready to show, or a private repo is made public.
- A featured repo is deleted, renamed, archived or made private.
- A featured project changes what it does, its stack, or ships a big feature, so its row no longer reads right.
- A headline in "About me" stops being true, such as a project that is finished or dropped.

Skip it for internal changes that do not change what a project does.

## What belongs in "Featured projects"

- Public repos only. A link to a private repo shows a 404 to visitors. Orion is the exception: link the public `Orion-Releases` repo.
- No forks, such as rojo, Maccy, luau-lsp or hq.
- No RoVault or StudioGit sync repos, game jam entries, tests or scratch projects.
- Roblox projects go under "Roblox". Everything else goes under "Tools and apps".

Check the current state with:

```bash
gh repo list nsawill1405 --limit 200 --json name,visibility,isFork,isArchived,description
```

## How to edit it

1. Clone `nsawill1405/nsawill1405` and read the current `README.md`.
2. Change only the rows or lines affected. Keep the existing layout, header images, badges and stats sections.
3. Each row is `| [**Name**](repo link) | What it does, one or two sentences | stack badges |`. Copy badge markup from an existing row with the same language.
4. Write the "What it does" text in William's voice and follow [[Unslop]]. Start from the repo description, and do not invent features.
5. Commit straight to `main` with a message such as `Add Whirl to featured projects`, since William asked for this to happen automatically. Follow the authorship rule in [[William North]].
6. Tell William what changed in your report.

If you cannot push to the repo, give William the exact change instead.

## Related

- [[Projects and Interests]]
- [[Writing Skills]]
