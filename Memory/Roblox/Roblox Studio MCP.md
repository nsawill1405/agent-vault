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
- Long generated commands can fail halfway and leave partial geometry. Rebuild generated folders from scratch instead of patching, and check console output and a screenshot before reporting.

## Related

- [[Roblox]]
