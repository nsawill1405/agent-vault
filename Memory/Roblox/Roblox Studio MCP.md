---
title: Roblox Studio MCP
type: memory
updated: "2026-11-25"
tags:
  - memory
  - roblox
  - mcp
---

# Roblox Studio MCP

Limits of the Roblox Studio MCP server.

- `Lighting.Technology` cannot be read from the MCP command thread. It needs `RobloxScript` capability.
- `save_place` cannot save a place that was never saved. It returns `NeedsUserAction` until William does one File > Save.
- In a Rojo project, anything built in Studio through MCP lives only in the place file and is lost on the next `rojo build`. Build geometry in code under `src/`, and use MCP for playtests, screenshots and place-level fixes such as deleting the template Baseplate.
- Studio drops to about 15 fps when its window is unfocused, so frame rates measured in an MCP playtest mislead. Hide the scene and measure again before blaming code.
- `screen_capture` needs a `capture_id`. Passing `camera_position` and `look_at_position` also works during a playtest.
- Long generated commands can fail halfway and leave partial geometry. Rebuild generated folders from scratch instead of patching, and check console output and a screenshot before reporting.

## Related

- [[Roblox]]
