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
- Animate EditableMesh vertices with one `mesh:BatchSetValues(vertexIds, positions)` call per frame, not a `SetPosition` per vertex. It also takes normal ids with `Vector3` values and colour ids with `Color3` values, so give each vertex its own `AddNormal` and `AddColor` id, bind them with `SetFaceNormals` and `SetFaceColors`, and update all three per frame.
- With StreamingEnabled, a client that pivots a server model (sway, bob) can grab the pivot before the parts arrive. `GetPivot()` then returns the origin and `PivotTo` drags the parts there. Make such models `ModelStreamingMode.Atomic` and wait for `PrimaryPart` before reading the pivot.
- Translucent water over a stepped seabed shows every step edge as a hard line. Use one sloped `WedgePart` instead.
- Check Luau types before Studio with `luau-lsp analyze --definitions=@roblox=globalTypes.d.luau --sourcemap=sourcemap.json src`. Make the sourcemap with `rojo sourcemap`. Download the definitions from luau-lsp's `scripts/globalTypes.d.luau`.
- Parallel actors cannot mutate instances. For part-heavy visual systems, measure main-thread update time before enabling workers; packing SharedTables and applying part properties can cost as much as the math being offloaded.
- Large SharedTable batch jobs should use contiguous numeric keys rather than generated string keys; string keys can erase the benefit of parallel work.

## Related

- [[Roblox]]
