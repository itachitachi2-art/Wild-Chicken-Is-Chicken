These are verification records for the exact shipped candidate DLL, not proof of in-game operation. Rebuilding changes the DLL hash; rerun the metadata audit for any rebuilt DLL.

Static audit (Python 3; no DLL execution):
python Verification/tools/audit_api.py --game-dll "<game>/7DaysToDie_Data/Managed/Assembly-CSharp.dll" --mod-dll WildChickenIsChicken/WildChickenIsChicken.dll --output fresh-api-audit.json

Isolated action/ABI model (Python 3 plus a trusted Mono C# compiler/runtime):
python Verification/isolated-tests/run.py --mcs "<path-to-mcs>" --mono "<path-to-mono>"

The model writes substitute Assembly-CSharp.dll files inside its test directories. These are invented test APIs, not game DLLs. Never copy its generated test directories into Mods. No test binaries or game runtime assemblies are included in this ZIP.

The production mod was built against supplied actual Managed assemblies, not against these substitutes. The checks do not exercise real UI, audio, world state, inventory, or Harmony interactions.
