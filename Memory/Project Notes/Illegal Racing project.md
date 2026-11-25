---
title: Illegal Racing project
type: memory
outcome: reference
updated: "2026-11-25"
tags:
  - memory
  - roblox
  - project
---

# Illegal Racing project

Illegal Racing is a greenfield Roblox arcade racing game. The authoritative design lives in `GDD.md` in the project repo.

## Scenario

The repo is `/Users/williamnorth/Downloads/illegal-racing`. On 25 November 2026 it contained only Fragua plugin scaffolding and a sample Zombie type. There were no racing, vehicle, data, UI or economy systems yet.

## What worked

Design the game as controlled chaos rather than unrestricted destruction:

- Use raycast suspension cars because the game is a fast arcade racer.
- Keep driven cars client-owned for responsive input, with server speed, teleport, hover and checkpoint validation.
- Use server-owned or anchored idle cars.
- Treat destruction in four classes: cosmetic props, structural props, terrain zones and hazards.
- Keep cosmetic debris client-only and pooled.
- Allow terrain edits only in marked zones, with server-side validation, merging, rate limits and round resets from snapshots.
- Use one active attachment per build, visible tradeoffs and a 6 point attachment budget.
- Use powerups as one-shot pickups weighted by race position.
- Avoid paid power and paid random items.

## Constraints

- Target server size is 10 players, with up to 10 racing.
- Launch scope is 8 cars, 15 attachments, 10 powerups and 3 tracks.
- Circuit Chaos and Time Trial are the launch modes. Wreck Race is post-launch.
- The design forbids open-world free roam, licensed cars, player-uploaded decals, trading and launch ranked matchmaking.
- Mobile input and performance are first-order constraints.

## Blackport Yard whitebox

The first track whitebox lives in the open Studio place as `Workspace.Whitebox_BlackportYard`. Layout version 4 was built after William asked for more height, a longer track, sharper turns, more loops, more randomness, smoother non-overlapping roads and a graybox material.

Useful facts:

- Main circuit centerline is about 5,494 studs across 32 control segments.
- Elevation range is 0 to 72 studs.
- Main road width is 32 studs. Shortcut widths are 14 to 18 studs.
- Ground cover is 1,700 by 1,700 studs, with outer boundary walls at about +/-820 studs.
- The route uses sharp outer zigzags, a southwest/central inner loop, and an intentional overpass near `(-350, 220)`.
- Alternate routes are an east container cut, a west warehouse cut, and a narrow high-level north bridge.
- Roads are continuous rounded ribbons generated with 6 quadratic samples per control-point corner. Main road uses 224 rounded samples.
- Checkpoint markers are open gate frames, not solid walls.
- Folder layout is `00_Ground` through `11_ElevatedRoadSupports`; all parts are gray `Concrete` and tagged `LF_Whitebox`.
- Road visual meshes currently use session-scoped opaque mesh content. Before relying on a saved place, convert them to uploaded mesh assets or durable part/union geometry.

Main circuit control points are `(x, z, elevation)`:

```text
(0,480,0) (230,480,0) (350,405,4) (500,450,9) (620,350,16)
(710,220,23) (760,70,31) (680,-50,40) (720,-180,47) (600,-300,55)
(450,-260,61) (380,-410,68) (200,-530,72) (0,-490,68) (-140,-560,62)
(-300,-520,57) (-430,-610,49) (-590,-520,42) (-500,-360,36) (-620,-220,29)
(-710,-50,21) (-590,80,16) (-660,240,10) (-500,330,7) (-360,220,9)
(-180,220,13) (-70,90,18) (-170,-20,24) (-330,20,30) (-350,170,30)
(-360,330,20) (-220,390,10) back to (0,480,0)
```

The place had never been saved when the whitebox was built, so Studio's save API could not save it automatically. William needs to save it once through File > Save before later saves can be automated.

## Fragua car driving proof

The first reusable car entity is a Fragua `Car` type backed by a `Model`. Source files live in the illegal-racing project:

- `ReplicatedStorage/Modules/CarControl.luau` defines the shared `{ throttle, steer }` input contract.
- `ReplicatedStorage/Modules/CarRig.luau` creates and validates `Root`, `DriveSeat`, wheel visuals and suspension attachments.
- `ReplicatedStorage/Modules/CarPhysics.luau` runs four-corner raycast suspension and accepts any input source.
- `ReplicatedStorage/Controllers/PlayerController.luau` supplies player input.
- `ServerStorage/Controllers/BotController.luau` supplies target/waypoint-following input through the same contract.
- `ReplicatedFirst/ClientLoader.local.luau` scans tagged Fragua cars and starts client physics only when the local player occupies the drive seat.
- `ServerStorage/Fragua/Types/CarServerBehavior.luau` owns rig creation, network ownership, idle anchoring and server bot physics.

Verified in Studio playtest:

- Player driving works with `W`; the car moved about 392 studs in 2.5 seconds and still had speed after key release.
- Bot driving works with `UseBotController = true` and `_FraguaRef_DriveTarget`; the server-owned car drove toward the target and reached about 97 studs/second.
- No client or server console errors remained after the final driving test.
- Roblox network ownership cannot be changed while the root is anchored. Unanchor first, then call `SetNetworkOwner`.
- Fragua client behavior startup is too timing-sensitive for seat occupancy. The normal client loader polling scan is more reliable and should stay the owner of player-driven client physics.
- `ReplicatedFirst` scripts can run before `ReplicatedStorage` children replicate. Use `WaitForChild` before requiring shared modules there.

## Related

- [[Memory Index]]
- [[Coding Principles]]
- [[Product and Game Design Taste]]
