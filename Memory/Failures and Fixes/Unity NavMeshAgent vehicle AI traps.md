---
title: Unity NavMeshAgent vehicle AI traps
type: memory
outcome: worked
updated: "2026-11-25"
tags:
  - memory
  - unity
  - navmesh
---

# Unity NavMeshAgent vehicle AI traps

Using `NavMeshAgent` as a path sensor for a fast `Rigidbody` vehicle requires disabling four movement flags, sampling lookahead along `path.corners` instead of `steeringTarget`, and guarding `Warp` and off-mesh links.

## Scenario

In `gears-game-jam` on Unity 6000.6.0f1, an AI car driven by `Rigidbody` physics used `NavMeshAgent` for pathfinding and `NavMeshLink` mode switches across `Drivable`, `Boatable`, and `Flyable` areas. Even with `updatePosition` and `updateRotation` disabled, the car still rotated unexpectedly, jerked to full steering lock at random angles along the road, and lost throttle on water.

## What failed

1. Setting `agent.destination` before `updatePosition = false` threw when `target` was unassigned, leaving default agent movement active. Leaving `agent.updateUpAxis` and `agent.autoTraverseOffMeshLink` at their `true` defaults also let Unity rotate the transform and slide across links.
2. Setting `agent.nextPosition = transform.position` and reading `agent.steeringTarget` in the same `Update` caused random full-lock steering spikes. Unity updates crowd corners between frames, so a `74 m/s` car regularly stepped past a path corner before `steeringTarget` advanced, placing `steeringTarget` behind the car and flipping `Atan2` near 180 degrees.
3. Calling `agent.Warp` when rebinding to a landing NavMesh teleported `transform.position` even with `agent.updatePosition = false`.
4. Running `dotnet build Assembly-CSharp.csproj` from the terminal failed inside cached Unity editor packages due to `ObjectPool` and `Image` symbol collisions outside the Editor build pipeline.

## What worked

- Disable `updatePosition`, `updateRotation`, `updateUpAxis`, `autoTraverseOffMeshLink`, `autoBraking`, and obstacle avoidance in `Awake`, and raise `agent.speed` and `agent.acceleration` above the vehicle top speed.
- Sample a pure-pursuit lookahead point `10m` to `24m` ahead along `agent.path.GetCornersNonAlloc`, stopping the lookahead at `agent.nextOffMeshLinkData.startPos` so the car lines up with bridges and ramps instead of cutting corners.
- Latch `OffMeshLink` traversal from `agent.isOnOffMeshLink` or `agent.nextOffMeshLinkData`, cast `owner` or `agent.navMeshOwner` to `Unity.AI.Navigation.NavMeshLink` to read `link.area`, freeze `nextPosition` updates until crossing the link exit plane, and save plus restore `transform.SetPositionAndRotation` around any off-mesh `agent.Warp`.
- Check `car.CameraAnchored` rather than `car.OnGround` for surface traction so `BoatMode` keeps throttle over deep water where wheel raycasts miss solid ground.
- For fast CLI compile verification in Unity 6 projects when Editor packages fail `dotnet build`, invoke Roslyn `csc.dll` directly with `Assembly-CSharp.csproj` `HintPath` references and `Library/ScriptAssemblies/*.dll`.
- Keep `Time.deltaTime` off `Input.GetAxis` mouse movement axes in `CameraController`, since `type: 1` mouse axes already return per-frame deltas.

## Related

- [[Memory Index]]
- [[Coding Principles]]
- [[Language Conventions]]
