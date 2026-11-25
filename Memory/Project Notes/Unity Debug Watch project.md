---
title: Unity Debug Watch project
type: memory
outcome: reference
updated: "2026-11-25"
tags:
  - memory
  - unity
  - project
---

# Unity Debug Watch project

`nsawill1405/unity-debug-watch` is a Unity 2021.3+ editor debugging package, and its only CI is a compile check against Unity 2021.1 reference DLLs.

## Scenario

Adding pre-release features (Preferences, shortcuts, saved layouts, build export) with no Unity Editor on the VM.

## What failed

- `[Shortcut]` commands for Freeze and Pause Graph would not fire in Play Mode while the Game view has focus, because Unity skips non-menu shortcuts there. They were changed to `[MenuItem("Tools/Debug Watch/...")]` with no key, so users bind them under Edit > Shortcuts > Main Menu.
- Running `tools/style_lint.py` on whole files reports hundreds of existing findings. Map `git diff -U0` hunks to finding line numbers and fix only the lines you added.

- The Devin GitHub app can't change repository visibility (HTTP 403). William has to make the repo private himself.

## What worked

- Compile every configuration in `Tools~/CompileCheck`: `DebugWatch.Editor.csproj`, `DebugWatch.Samples.csproj`, the same with `-p:PlayerBuild=true`, and with `-p:PlayerBuild=true -p:DebugWatchBuild=true`.
- Editor state that must survive restarts uses `ScriptableSingleton<T>` with `[FilePath("UserSettings/...", Location.ProjectFolder)]` and an explicit `Save(true)` on change, quit and assembly reload.
- Never call `Object.GetInstanceID()`. William's Unity version rejects it, and the 2021 compile check does not catch it.
- Version bumps touch `package.json`, `DebugWatchInfo.Version` (the Asset Store build script fails if it differs), the `#vX.Y.Z` install URLs in `README.md`, and a new `CHANGELOG.md` entry.
- EditMode tests in `Tests/Editor` also run outside Unity with `dotnet test Tools~/CompileCheck/Tests/DebugWatch.Tests.csproj`, as long as they avoid calls into native engine code (EditorPrefs, LayerMask names). Set `TimeSeries.KeepAll` in tests to skip the EditorPrefs read.
- The test project lives in its own `Tests/` subfolder because the CompileCheck projects share one `obj/` folder, and a net8.0 project there breaks the netstandard2.1 restore.
- `python3 "Tools~/AssetStore/build_store_package.py"` builds the Asset Store copy under `Assets/DebugWatch` and a `.unitypackage`.

## Related

- [[Memory Index]]
- [[Coding Principles]]
- [[Workflow Preferences]]
