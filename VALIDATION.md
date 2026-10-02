# v0.1.2 validation

- Compiled successfully with Mono C# 6.8 against the supplied game Managed assemblies, using `/nostdlib+`. This checks the real game API signatures; the Windows build.cmd execution has not been run here.
- Assembly-CSharp.dll SHA-256: `cb33a4adbd9bd25c98255b8de675b3050ea39c782a515ec97cf943eac4a480fe`.
- The Windows build remains Framework csc + game runtime assemblies, command-line `/noconfig`, and a UTF-8 response file. Added UnityEngine.IMGUIModule.dll and UnityEngine.TextRenderingModule.dll only for presentation.
- Sound group `chickendeath` is present in the supplied vanilla sounds.xml. Audio.Manager.Play(Entity, string, float, bool) was verified in the game assembly.
- Verified SaveAndCleanupWorld raises WorldShuttingDown before SaveLocalPlayerData. Accepted rewards are flushed by that event when exiting early.

Nine isolated checks using the actual feedback source and minimal game/UI substitutes passed:

1. No sound or items before 2 seconds.
2. Sound request precedes chicken and feather delivery.
3. Repeated updates do not duplicate rewards or sound.
4. Occupied original slots are preserved after switching/moving items.
5. Partial feather insertion drops only the remainder.
6. Temporarily unavailable UI retries rewards without repeating sound.
7. A different world does not receive old rewards.
8. Shutdown flush preserves ordering and prevents duplicates.
9. A sound API exception does not lose accepted rewards.

In-game validation is still required for actual rendering, audible playback, movement/switching during the bar, overflow delivery, and immediate exit/reload. These checks do not claim gameplay verification. Abrupt process termination during the two-second interval cannot run the shutdown flush.
