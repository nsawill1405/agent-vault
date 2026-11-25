---
title: Roblox engine
type: memory
updated: "2026-11-25"
tags:
  - memory
  - roblox
---

# Roblox engine

Roblox engine traps.

- `SetNetworkOwner` fails while the root part is anchored. Unanchor first.
- `ReplicatedFirst` scripts can run before `ReplicatedStorage` children replicate. Use `WaitForChild` before requiring shared modules there.
- `Terrain:GetOccupancyRegion()` does not exist and `Enum.PartType.Cone` does not exist.
- `CreateMeshPartAsync(Content.fromObject(editableMesh))` links the live EditableMesh. Destroying the editable makes the MeshPart invisible.
- To bake an EditableMesh, call `AssetService:CreateDataModelContentAsync`, check for `Enum.CreateContentResult.Success`, then pass the content to `CreateMeshPartAsync`. That content is still session-only. Meshes that must survive a save need `CreateAssetAsync` uploads or geometry rebuilt from data.
- `UnionAsync` unions of segmented road pieces stay visibly faceted.

## Related

- [[Roblox]]
