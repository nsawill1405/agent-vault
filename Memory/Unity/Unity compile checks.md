---
title: Unity compile checks
type: memory
updated: "2026-11-25"
tags:
  - memory
  - unity
---

# Unity compile checks

How to compile Unity packages on a machine without the Editor.

- Agent VMs have no Unity Editor and no dotnet. Install .NET 8 with `dotnet-install.sh` and build against the `Unity3D.SDK` 2021.1.14.1 NuGet package, with `NU1701` in `NoWarn`.
- The 2021.1 reference DLLs are older than the package minimum of 2021.3. Wrap 2021.2+ APIs such as `ShortcutModifiers.Control` in `#if UNITY_2021_2_OR_NEWER`. Check API availability in the `Unity-Technologies/UnityCsReference` branches with `gh api`.
- In Unity 6 projects where `dotnet build Assembly-CSharp.csproj` fails on cached package symbol collisions (`ObjectPool`, `Image`), run Roslyn `csc.dll` directly with the csproj `HintPath` references and `Library/ScriptAssemblies/*.dll`.

## Related

- [[Unity]]
