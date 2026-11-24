---
title: Language Conventions
type: profile
tags:
  - william
  - coding
---

# Language Conventions

Part of [[William North]]. General rules are in [[Coding Principles]].
Follow a repo's own config files first. These are the defaults when a repo has none.

## Luau and Roblox (observed)

- Lint with Selene using `std = "roblox"`.
- Format with StyLua using this config, taken from Hitbox-Plus:

```toml
column_width = 100
line_endings = "Unix"
indent_type = "Tabs"
indent_width = 4
quote_style = "AutoPreferSingle"
call_parentheses = "Always"
```

- Use Rojo for syncing files into Studio.
- Use strict type annotations where the code is public API.
- Keep constants at the top of the module in UPPER_SNAKE_CASE.
- Studio plugins should clean up connections and widgets when unloaded.

## C# and Unity (observed)

- Named `const` values with PascalCase, like `DefaultLength` and `UvPerUnit`.
- Explicit generic types, like `List<Vector3>`, rather than `var` for fields.
- Editor tools live in an `Editor/` folder and must cost nothing in builds. Strip debug code with conditional compilation.
- Keep editor windows responsive. Cache reflection results.

## TypeScript and React (observed)

- Declare named types for messages, payloads, and props.
- Avoid `any`. Use `unknown` and narrow it.
- Prefer plain functions and small components over clever abstractions.

## Python (observed)

- Use plain loops over dense comprehensions when the logic has more than one condition.
- Standard library first. Add a dependency only when it removes real work.
- Type hints on public functions.

## Swift and macOS (observed)

William builds small native macOS utilities, like dustpan and clipdesk.
Keep them native, light, and focused on one annoyance.
