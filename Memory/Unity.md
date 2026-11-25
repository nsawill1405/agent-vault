---
title: Unity
type: memory
updated: "2026-11-25"
tags:
  - memory
  - unity
---

# Unity

Cross-project Unity lessons. Repo-specific facts live in each repo's `AGENTS.md`.

## Compiling without the Editor

- Agent VMs have no Unity Editor and no dotnet. Install .NET 8 with `dotnet-install.sh` and build against the `Unity3D.SDK` 2021.1.14.1 NuGet package, with `NU1701` in `NoWarn`.
- The 2021.1 reference DLLs are older than the package minimum of 2021.3. Wrap 2021.2+ APIs such as `ShortcutModifiers.Control` in `#if UNITY_2021_2_OR_NEWER`. Check API availability in the `Unity-Technologies/UnityCsReference` branches with `gh api`.
- In Unity 6 projects where `dotnet build Assembly-CSharp.csproj` fails on cached package symbol collisions (`ObjectPool`, `Image`), run Roslyn `csc.dll` directly with the csproj `HintPath` references and `Library/ScriptAssemblies/*.dll`.

## API traps

- Never call `Object.GetInstanceID()`. William's Unity version rejects it with CS0619 ("Use GetEntityId instead") and the 2021 compile check does not catch it. Key by reference, or use `GetHashCode()` when a key must survive domain reloads.
- `[Shortcut]` commands do not fire while a playing, unpaused Game view has focus. Use `[MenuItem("Menu/Path _F1")]` for hotkeys that must work in Play Mode. Rebind a menu hotkey through the shortcut id `"Main Menu/" + menuPath`.
- Editor state that must survive restarts: `ScriptableSingleton<T>` with `[FilePath("UserSettings/...", Location.ProjectFolder)]`, and call `Save(true)` on change, quit and assembly reload.
- Trigger callbacks get the child `Collider`, not the root. Resolve components with `other.GetComponentInParent<T>()` and debounce per root object when it has several colliders.
- `Input.GetAxis` mouse axes already return per-frame deltas. Do not multiply them by `Time.deltaTime`.

## NavMeshAgent as a path sensor for a Rigidbody vehicle

- In `Awake`, turn off `updatePosition`, `updateRotation`, `updateUpAxis`, `autoTraverseOffMeshLink`, `autoBraking` and obstacle avoidance before setting a destination. Set `agent.speed` and `agent.acceleration` above the vehicle top speed.
- Do not steer at `agent.steeringTarget` on fast vehicles. It lags a frame behind, ends up behind the car and causes full-lock spikes. Sample a lookahead point along `agent.path.GetCornersNonAlloc` instead.
- `agent.Warp` moves the transform even with `updatePosition = false`. Save and restore `transform.SetPositionAndRotation` around it.
- `agent.radius` changes at runtime do not widen corners, because the bake erodes the NavMesh. Center the lookahead with lateral `NavMesh.Raycast` probes instead.
- Gate `OffMeshLink` entry by vertical distance, not XZ distance alone, or links above the car trigger when it drives underneath.

## Related

- [[Memory Index]]
