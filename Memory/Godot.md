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
- A focused `Button` takes Tab for focus cycling before `_unhandled_input` sees it. Read a Tab-bound action in `_input`, or set `focus_mode = FOCUS_NONE` on mouse-only buttons.
- SVG UI art imported at `svg/scale=2.0` stays sharp on high-DPI screens. Divide the texture size by the same scale for layout, and set it in every new `.import` file.
- Headless Godot cannot screenshot. Run under `xvfb-run` with a `--script` that loads the main scene, waits about 150 frames, then saves `get_viewport().get_texture().get_image()`.
