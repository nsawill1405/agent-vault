---
title: Roblox Studio MCP traps
type: memory
outcome: reference
updated: "2026-11-25"
tags:
  - memory
  - roblox
  - studio
  - mcp
---

# Roblox Studio MCP traps

Traps hit while building the Illegal Racing whitebox.

## API and enum traps

- `Terrain:GetOccupancyRegion()` is not available. Do not use it for terrain validation.
- `Enum.PartType.Cone` does not exist. Use `Block`, `Cylinder`, `Wedge`, or a `MeshPart` instead.
- `Lighting.Technology` cannot be read from the MCP command thread because it requires `RobloxScript` capability.
- Asset pack scattering through asset id `95206881` failed while cloning. Treat that pack path as unreliable until it is verified again.

## Broken LihFolk vault path

The vault beside the installed skill at `~/.agents/skills/lihfolk/../../LihFolk Vault V2` is incomplete and its search tools can fail with `ZeroDivisionError`. The working local vault is:

```text
/Users/williamnorth/Downloads/LIH/LihFolk Vault V2/LihFolk Vault V2
```

Use `python3` with its `_tools/vault.py` helper.

## Saving places

`save_place` cannot save a place that has never been saved. It returns `NeedsUserAction` and asks for one manual File > Save first. After that first save, later saves can be automated.

## Validation habit

Long generated Studio commands can fail halfway and leave partial geometry. Rebuild generated whitebox folders from scratch instead of trying to patch duplicates, and check console output plus screenshots before reporting the result.
