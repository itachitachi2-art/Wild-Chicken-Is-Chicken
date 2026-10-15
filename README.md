# Current delivery: Wild Chicken Is Chicken v0.1.3-test1

2026-10-15: imported the already-delivered source, verification records and exact runtime ZIP. No rebuild or gameplay change was made during this sync. This is a test candidate; native gameplay remains unverified.

[Download the installable ZIP](dist/WildChickenIsChicken-v0.1.3-test1-v3.3-install.zip) · [Import identity](docs/SYNC-20261015.json)

The following is the delivered development documentation. Historical references describe their recorded stage.

---

# Wild Chicken Is Chicken v0.1.3-test1 for 7 Days to Die v3.3

Private compatibility test build. This is not a published release and has not been tested inside the game.

## What changed

Rebuilt the v0.1.2 gameplay source against the supplied v3.3 game Managed assemblies. In these assemblies, ItemInventoryData.holdingEntity is a property rather than the field expected by an older binary. The rebuilt DLL calls get_holdingEntity. The compiled references for slotIdx, itemStack, ItemStack.count/itemValue, and ItemValue.type also use the current accessors.

The slaughter action, two-second presentation, rewards, configuration, recipes, and artwork are unchanged. Changes to source are limited to build identity and the startup log. ModInfo reports 0.1.3; the startup log identifies v0.1.3-test1.

This matches the reported MissingFieldException mechanism. The reporter's installed DLL and exact game build have not been inspected, so this is a candidate fix, not proof that every reported error came from this mod.

## Install the test build

1. Close the game. Back up the save and the existing WildChickenIsChicken mod folder.
2. Replace the old WildChickenIsChicken folder with the folder of the same name in this ZIP. Do not keep two copies of the mod or mix old and new DLLs.
3. Start 7 Days to Die v3.3 with EAC disabled.
4. Confirm the log contains `[WildChickenIsChicken] v0.1.3-test1 loaded`.
5. Test on a disposable save first: capture/carry a chicken, press and release secondary action, confirm the bar and sound then one butchered chicken plus 23 feathers. Check moving/switching items during the bar, full inventory fallback, coop placement, and save/reload.
6. If the same error remains, retain the full log from startup through the error, exact game version, installed mod version/file, and other installed mods for diagnosis.

To roll back, close the game and restore the previous mod folder and, if necessary, the backed-up test save. This package does not modify or install anything automatically.

## Build from source

The compiled DLL is already included. On Windows, `build.cmd "D:\SteamLibrary\steamapps\common\7 Days To Die"` rebuilds against that exact game's Managed assemblies using the Windows Framework C# compiler. Prefer an explicit v3.3 game path if several installations exist. `build-release.cmd` creates another install ZIP. Building against v3.2 will produce v3.2 field references again; do not redistribute such a DLL as the v3.3 candidate. The version label alone does not establish API compatibility.

Game runtime DLLs and Harmony are not included. The mod uses the game's ItemAction extension point and installs no Harmony patches.

## Verification

See VALIDATION.md and Verification/ for the exact reference hashes, candidate DLL identity, metadata audit, source provenance, and isolated regression logs. No claim of in-game, multiplayer, dedicated-server, or cross-mod compatibility is made.
