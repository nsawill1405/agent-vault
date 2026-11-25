---
title: Illegal Racing
type: memory
updated: "2026-11-25"
tags:
  - memory
  - roblox
  - project
---

# Illegal Racing

Roblox arcade racing game. The repo is only on William's Mac at `~/Downloads/illegal-racing`, so its notes live here. Move them into the repo's `AGENTS.md` once it is on GitHub.

- `GDD.md` in the repo is the design authority. Read it before design work.
- Cars use raycast suspension. Driven cars are client-owned with server speed, teleport, hover and checkpoint checks. Idle cars are server-owned or anchored.
- One input contract, `{ throttle, steer }` in `ReplicatedStorage/Modules/CarControl.luau`, feeds both `PlayerController` and `BotController`. `CarPhysics.luau` accepts any input source.
- The car is a Fragua `Car` type backed by a `Model`. `CarServerBehavior.luau` owns rig creation, network ownership, idle anchoring and bot physics.
- `ReplicatedFirst/ClientLoader.local.luau` starts client physics only when the local player sits in the drive seat. Keep it as the owner of player-driven physics.
- Whitebox parts are gray `Concrete` tagged `LF_Whitebox`, in folders `00_Ground` to `11_ElevatedRoadSupports`. Rebuild the whitebox from scratch rather than patching it.

## Related

- [[Memory Index]]
- [[Roblox]]
