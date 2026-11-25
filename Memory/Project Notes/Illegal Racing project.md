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

## Related

- [[Memory Index]]
- [[Coding Principles]]
- [[Product and Game Design Taste]]
