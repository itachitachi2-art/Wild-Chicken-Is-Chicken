# Wild Chicken Is Chicken v0.1.1

**Wild chickens are chickens. Catch it. Raise it. Or eat it.**

A small mod for 7 Days to Die v3.2. Carry captured wild chickens to the coop as usual, or press and release the secondary action to obtain one Butchered Chicken and 23 feathers. Overflow feathers drop on the ground.

Butchered Chicken can be used in the existing chicken wings, ash chicken stew, and roadrunner chicken jerky recipes. It cannot be used in a coop. Wild chicken MoveSpeedPanic is adjusted from 1.5 to 1.2. Other hunting and coop production settings remain unchanged.

## Build and install

On Windows, run `build.cmd`, then copy the built `WildChickenIsChicken` folder to your Mods directory. Disable EAC. No .NET SDK is required: the build uses Windows Framework csc and the game-provided runtime assemblies.

Run `build-release.cmd` to generate `WildChickenIsChicken-v0.1.1-install.zip` containing the compiled mod DLL and runtime assets. Game runtime DLLs are never included.

## Verification

User gameplay testing confirmed capture, carrying, slaughter, cooking, feather collection, the custom icon, and continued coop production. Inventory-overflow feather drops have not been separately reported. Multiplayer, dedicated servers, and compatibility with other chicken mods remain unverified.

Japanese item name: 絞めたニワトリ. English item name: Butchered Chicken. Both descriptions are provided.

The reported “Meep! Meep!” message remains under observation; no related changes are included.

See `WildChickenIsChicken/README.txt` for Japanese installation and gameplay instructions.
