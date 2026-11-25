---
title: Unity NavMeshAgent vehicles
type: memory
updated: "2026-11-25"
tags:
  - memory
  - unity
  - navmesh
---

# Unity NavMeshAgent vehicles

Using a NavMeshAgent as a path sensor for a Rigidbody vehicle.

- In `Awake`, turn off `updatePosition`, `updateRotation`, `updateUpAxis`, `autoTraverseOffMeshLink`, `autoBraking` and obstacle avoidance before setting a destination. Set `agent.speed` and `agent.acceleration` above the vehicle top speed.
- Do not steer at `agent.steeringTarget` on fast vehicles. It lags a frame behind, ends up behind the car and causes full-lock spikes. Sample a lookahead point along `agent.path.GetCornersNonAlloc` instead.
- `agent.Warp` moves the transform even with `updatePosition = false`. Save and restore `transform.SetPositionAndRotation` around it.
- `agent.radius` changes at runtime do not widen corners, because the bake erodes the NavMesh. Center the lookahead with lateral `NavMesh.Raycast` probes instead.
- Gate `OffMeshLink` entry by vertical distance, not XZ distance alone, or links above the car trigger when it drives underneath.

## Related

- [[Unity]]
