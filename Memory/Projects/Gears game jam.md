---
title: Gears game jam
type: memory
updated: "2026-11-25"
tags:
  - memory
  - unity
  - project
---

# Gears game jam

Unity 6000.6.0f1 game, `nsawill1405/gears-game-jam`. Devin cannot push there, so its notes live here. General NavMesh lessons are in [[Unity]].

- AI cars switch modes over `NavMeshLink` areas `Drivable`, `Boatable` and `Flyable`. Read `link.area` by casting `owner` or `agent.navMeshOwner` to `Unity.AI.Navigation.NavMeshLink`.
- `BoatMode` cuts propulsion when `overDryLand` is true. Switch a `Boatable` link back to `Car` as soon as `IsInDeepWater` turns false, and check `car.CameraAnchored` rather than `car.OnGround` for traction over deep water.
- A boat stranded in open water with no water-level NavMesh should score scene `NavMeshLink` endpoints near water height by sail distance plus `NavMesh.CalculatePath` length to the target.
- Compile-check from the terminal with Roslyn `csc.dll` directly. `dotnet build` fails on cached package symbol collisions.

## Related

- [[Memory Index]]
