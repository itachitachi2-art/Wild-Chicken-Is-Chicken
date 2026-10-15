# v0.1.3-test1 validation

## Scope and evidence

- Source base: GitHub commit 285f589d186db58d8ff20e1bb2bf627c1825c73d (v0.1.2).
- The action and feedback C# files are byte-for-byte unchanged from that commit. Configuration and artwork are unchanged.
- Only version identity, startup logging, packaging labels, and documentation changed.
- Compiled successfully without warnings using Mono C# 6.12.0.199, /noconfig and /nostdlib+, and the actual supplied v3.3 game runtime assemblies. No game/API doubles were used in the production DLL build.
- Target Assembly-CSharp.dll SHA-256: fceec27300ffd3a1f97b097e43b60f3b07597f441e7ecbc6e1b59eebb234c705.
- Historical v0.1.2 validation recorded a different reference SHA-256: cb33a4adbd9bd25c98255b8de675b3050ea39c782a515ec97cf943eac4a480fe.
- Candidate DLL SHA-256: 4f4016c9c158900a6189a245c197e0bdf7ae1746245413c4736e06f758f08061.
- Candidate assembly/file version: 0.1.3.0; informational version: 0.1.3-test1-v3.3.
- All 40 Assembly-CSharp MemberRef records match supplied game metadata by member kind and signature. All 21 method bodies parse successfully. There are no stale critical field references. ExecuteAction calls ItemInventoryData.get_holdingEntity.

## Isolated regression model

The actual ItemActionWCICButcherChicken.cs source was compiled with minimal substitute APIs. This is not a game execution test.

Eleven checks passed against a field-shaped API, and the same eleven passed against a property-shaped API:

1. Release without press does not consume.
2. Press alone does not consume.
3. Press/release accepts one chicken.
4. 23 feathers are prepared.
5. One butchered chicken is prepared.
6. Repeated release does not duplicate.
7. StopHolding disarms the press.
8. A non-primary player is rejected.
9. An unexpected stack count is rejected.
10. A dead player is rejected.
11. Missing UI is rejected before consumption.

Running the field-compiled action against the property-only substitute recreated exactly:

MissingFieldException: Field not found: EntityAlive .ItemInventoryData.holdingEntity Due to: Could not find field in class

Recompiling against the property API passed. This proves the failure mechanism in isolation; it does not identify the reporter's installed DLL.

## Not verified

The reporter's full log, exact game build, and installed DLL were not available for comparison. The game, Unity, and actual game assemblies were never executed. Windows build.cmd was not executed. Actual UI rendering, sound, inventory mutation, animation timing, save/reload, multiplayer, dedicated servers, and interaction with other mods remain untested for this candidate. The isolated feedback tests documented historically for v0.1.2 were not rerun and are not counted here.

## Evidence files

Verification/build-verification.json records source/reference hashes and compiler invocation. Verification/candidate-api-audit.json records the metadata and emitted calls. Verification/source-provenance.json compares source/assets with the base commit. Verification/isolated-tests contains test source and logs without compiled game substitutes or reference DLLs. Only the mod DLL is distributed.
