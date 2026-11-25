---
title: Roblox
type: memory
updated: "2026-11-25"
tags:
  - memory
  - roblox
---

# Roblox

Cross-project Roblox and Roblox Studio lessons. Repo-specific facts live in each repo's `AGENTS.md`.

## Engine

- `SetNetworkOwner` fails while the root part is anchored. Unanchor first.
- `ReplicatedFirst` scripts can run before `ReplicatedStorage` children replicate. Use `WaitForChild` before requiring shared modules there.
- `Terrain:GetOccupancyRegion()` does not exist and `Enum.PartType.Cone` does not exist.
- `CreateMeshPartAsync(Content.fromObject(editableMesh))` links the live EditableMesh. Destroying the editable makes the MeshPart invisible.
- To bake an EditableMesh, call `AssetService:CreateDataModelContentAsync`, check for `Enum.CreateContentResult.Success`, then pass the content to `CreateMeshPartAsync`. That content is still session-only. Meshes that must survive a save need `CreateAssetAsync` uploads or geometry rebuilt from data.
- `UnionAsync` unions of segmented road pieces stay visibly faceted.

## Studio MCP

- `Lighting.Technology` cannot be read from the MCP command thread. It needs `RobloxScript` capability.
- `save_place` cannot save a place that was never saved. It returns `NeedsUserAction` until William does one File > Save.
- Long generated commands can fail halfway and leave partial geometry. Rebuild generated folders from scratch instead of patching, and check console output and a screenshot before reporting.

## Fragua

- Fragua client behavior startup is too timing-sensitive for seat occupancy. Start player-driven client physics from a polling loader script instead.

## RoVault

- Do not stamp bookkeeping data, such as an id attribute, onto instances in the user's place. Match same-named siblings to their saved copies on GitHub instead (stated).

## Related

- [[Memory Index]]
