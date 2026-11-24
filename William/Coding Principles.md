---
title: Coding Principles
type: profile
tags:
  - william
  - coding
---

# Coding Principles

Part of [[William North]]. Language specifics live in [[Language Conventions]].
The linter in `tools/style_lint.py` checks some of these rules automatically. See [[Style Linter]].

## Simple, longer code over one-liners (stated)

William prefers code that takes more lines but reads in one pass.
A reviewer should be able to explain each line out loud and set a breakpoint on it.

Do this:

```python
active_players = []
for player in players:
    if player.is_alive and not player.is_spectating:
        active_players.append(player)
```

Not this:

```python
active_players = [p for p in players if p.is_alive and not p.is_spectating] if players else []
```

Concrete rules:

- One idea per line. Split chained calls, nested ternaries, and long boolean expressions into named steps.
- No nested ternaries. Use `if` and `else`.
- No nested comprehensions or lambdas inside comprehensions. Use a loop.
- Name intermediate values. A variable called `is_ready_to_spawn` explains more than a comment.
- Prefer early returns over deep nesting.
- Keep functions short enough to read without scrolling, but do not split code into tiny helpers just to look tidy.

## No load-bearing hacks (stated)

Code must not depend on something fragile that nobody would think to protect.

- No magic numbers. Give values a named constant, like `DEFAULT_ROAD_WIDTH` or `UvPerUnit` in his Unity code.
- No silent fallbacks that hide errors. Fail loudly with a clear message.
- No swallowed exceptions (`except: pass`, empty `catch {}`).
- No reliance on timing, `wait()` calls, or execution order unless it is documented and enforced.
- No hard-coded special cases to make a test pass. Fix the general behavior.
- If a workaround is truly needed, mark it with a comment that says why and when it can go.

## Explicit types and structure (observed)

His TypeScript, C#, and Luau code declares types and data shapes up front.
Examples: named `MessageRole`, `Attachment`, and `ChatMessage` types in Orion, and typed `List<Vector3>` fields in the Unity road extruder.

- Declare types for public functions and data structures.
- Prefer a small named struct or type over a loose dictionary.
- Keep ordered lists of things (like Roblox class lists in Fragua) as explicit, readable tables.

## Lint and format everything (stated and observed)

Every repo should have a linter and a formatter wired into CI.
Luau repos use Selene and StyLua. If a project has no linter, add one rather than skipping the check.

## Comments

- Default to no comment. Good names come first.
- Comment the why, not the what.
- Every non-obvious constant and every workaround gets a short reason.
