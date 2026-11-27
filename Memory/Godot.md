---
title: Godot
type: memory
updated: "2026-11-27"
tags:
  - memory
  - godot
---

# Godot

Lessons from Godot 4 GDScript projects.

- Godot exits 0 when a script fails to parse. Grep the output of `--headless --quit-after 60` for `SCRIPT ERROR|Parse Error` instead of trusting the exit code.
- With warnings as errors, `var x := ui.some_method()` fails when the callee is untyped. Write the type: `var x: bool = ui.some_method()`.
- A helper object that takes its owner in `new()` must type the owner as `Node` when the owner is a `CanvasLayer`. `Control` is rejected.
- When splitting a big script with a Python script, check the line count before committing. A bad slice can repeat the file thousands of times. Restore with `git checkout <file>` and redo it.
- For click-through overlays, poll the mouse each frame and set `WINDOW_FLAG_MOUSE_PASSTHROUGH` to `not over_any_interactive_rect`. This is simpler than a passthrough polygon, and moving targets keep working.
- Cap `content_scale_factor` at `usable_height / view_height`. Otherwise high zoom on a high-DPI screen pushes the top of a bottom-anchored window off screen.
- A wrapping `Label` in a container collapses to zero width. Set `custom_minimum_size.x` to the smaller of the text width and the space available.
- A balance simulator that plays greedily through the real `can_buy` and `buy` code catches progression that is far too fast. Run it after every cost change.
- Rebuilding a container's children with only `queue_free()` leaves the old rows in the tree until the end of the frame, so `reset_size()` still counts them. Call `remove_child(child)` before `queue_free()`.
- To tell when a list panel needs rebuilding, keep a `duplicate(true)` of the data it last drew and compare it to the live data. Comparing child counts loops forever while freed rows are still in the tree.
- A focused `Button` takes Tab for focus cycling before `_unhandled_input` sees it. Read a Tab-bound action in `_input`, or set `focus_mode = FOCUS_NONE` on mouse-only buttons.
- SVG UI art imported at `svg/scale=2.0` stays sharp on high-DPI screens. Divide the texture size by the same scale for layout, and set it in every new `.import` file.
- Headless Godot cannot screenshot. Run under `xvfb-run` with a `--script` that loads the main scene, waits about 150 frames, then saves `get_viewport().get_texture().get_image()`.
- A `CanvasModulate` darkens everything on its canvas layer, so night lighting with `PointLight2D` needs the HUD on its own `CanvasLayer`. Use `light_mask` bits so the lantern lights only nearby layers.
- Without `rsvg-convert`, preview SVG art with a small Godot `--script` that calls `Image.load_svg_from_string()` and saves a PNG.
- Do not add per-frame wobble to a value that is also smoothed with `lerpf(value, target, rate * delta)`. The wobble feeds back and grows about `1 / (rate * delta)` times. Smooth a separate variable and add the wobble on output.
- A new test file does nothing until it is listed in `tests/run_tests.gd`. If another slice owns that file, put the exact line in the PR's integration notes.
- Godot gives no warning when `theme_type_variation` names a type the theme does not define, and the control can render with no visible text. Check each variation string against the theme's type names.
- For click-driven minigames, record presses in `_input()` and consume them in `_process()`. Polling `Input.is_mouse_button_pressed()` misses quick clicks. Judge each click against the state the player saw before moving anything.
- Meters filled by fixed float steps can stop just short of 1.0 (0.3 + 7 × 0.1 = 0.9999…). Test against `1.0 - 1e-6`, not `1.0`.
- An autowrapped `Label` only gets its real height after one layout pass, so a new wrapped panel shows at the wrong size for one frame. Keep it at `modulate.a = 0.0` for its first tick; `reset_size()` does not fix it.
- Cooldowns that should outlast a relaunch, such as "one rare event per hour of play", belong in the saved state and count down with play time. A timer in the scene restarts on every launch.
- In idle games, when a perk changes what one worker earns in the live sim, add it to the analytic income formula too, or offline pay silently ignores it.
