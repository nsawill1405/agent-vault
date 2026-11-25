---
title: Unity API traps
type: memory
updated: "2026-11-25"
tags:
  - memory
  - unity
---

# Unity API traps

Unity APIs that behave in ways agents get wrong.

- Never call `Object.GetInstanceID()`. William's Unity version rejects it with CS0619 ("Use GetEntityId instead") and the 2021 compile check does not catch it. Key by reference, or use `GetHashCode()` when a key must survive domain reloads.
- `[Shortcut]` commands do not fire while a playing, unpaused Game view has focus. Use `[MenuItem("Menu/Path _F1")]` for hotkeys that must work in Play Mode. Rebind a menu hotkey through the shortcut id `"Main Menu/" + menuPath`.
- Editor state that must survive restarts: `ScriptableSingleton<T>` with `[FilePath("UserSettings/...", Location.ProjectFolder)]`, and call `Save(true)` on change, quit and assembly reload.
- Trigger callbacks get the child `Collider`, not the root. Resolve components with `other.GetComponentInParent<T>()` and debounce per root object when it has several colliders.
- `Input.GetAxis` mouse axes already return per-frame deltas. Do not multiply them by `Time.deltaTime`.

## Related

- [[Unity]]
- [[Unity compile checks]]
