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
- EditableMesh fails in published games until Allow Mesh / Image APIs is on (Studio Experience Settings > Security, or the dashboard's Configure > Settings).
- `AssetService:CreateEditableMesh()` returns nil when the client's editable memory budget is used up. Check for nil.
- EditableMesh faces render from the side where vertices go counterclockwise. For an upward-facing grid at (x = column, z = row), add `(v[r][c], v[r+1][c], v[r][c+1])` and `(v[r][c+1], v[r+1][c], v[r+1][c+1])`.
- Animate EditableMesh vertices with one `mesh:BatchSetValues(vertexIds, positions)` call per frame, not a `SetPosition` per vertex.
- Check Luau types before Studio with `luau-lsp analyze --definitions=@roblox=globalTypes.d.luau --sourcemap=sourcemap.json src`. Make the sourcemap with `rojo sourcemap`. Download the definitions from luau-lsp's `scripts/globalTypes.d.luau`.

## Related

- [[Roblox]]
