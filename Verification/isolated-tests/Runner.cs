using System;
public static class Runner {
    private static int passed;
    static void Check(bool condition, string name) { if (!condition) throw new Exception("FAILED: " + name); ++passed; Console.WriteLine("PASS: " + name); }
    static void Run() {
        var action = new ItemActionWCICButcherChicken();
        var data = action.CreateModifierData(GameHarness.Prepare(true, 1, false, true), 1);
        action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 0, "release without press does not consume");
        action.ExecuteAction(data, false);
        Check(GameHarness.Accepted == 0, "press alone does not consume");
        action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 1, "press-release accepts one chicken");
        Check(WCICButcherFeedback.Instance.Accepted[0].Feathers.count == 23, "23 feathers prepared");
        Check(WCICButcherFeedback.Instance.Accepted[0].Chicken.count == 1, "one butchered chicken prepared");
        action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 1, "repeated release does not duplicate");
        data = action.CreateModifierData(GameHarness.Prepare(true, 1, false, true), 1);
        action.ExecuteAction(data, false); action.StopHolding(data); action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 0, "StopHolding disarms pending press");
        data = action.CreateModifierData(GameHarness.Prepare(false, 1, false, true), 1);
        action.ExecuteAction(data, false); action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 0, "remote or non-primary player rejected");
        data = action.CreateModifierData(GameHarness.Prepare(true, 2, false, true), 1);
        action.ExecuteAction(data, false); action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 0, "unexpected stack count rejected");
        data = action.CreateModifierData(GameHarness.Prepare(true, 1, true, true), 1);
        action.ExecuteAction(data, false); action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 0, "dead player rejected");
        data = action.CreateModifierData(GameHarness.Prepare(true, 1, false, false), 1);
        action.ExecuteAction(data, false); action.ExecuteAction(data, true);
        Check(GameHarness.Accepted == 0, "missing UI rejected before consumption");
        Console.WriteLine("PASSED " + passed);
    }
    public static int Main(string[] args) {
        bool expectMismatch = args.Length > 0 && args[0] == "expect-mismatch";
        try { Run(); if (expectMismatch) { Console.WriteLine("ERROR: mismatch did not occur"); return 1; } return 0; }
        catch (MissingFieldException e) { Console.WriteLine(e.ToString()); if (expectMismatch && e.Message.Contains("holdingEntity")) { Console.WriteLine("EXPECTED_ABI_FAILURE_CONFIRMED"); return 0; } return 1; }
        catch (Exception e) { Console.WriteLine(e.ToString()); return 1; }
    }
}
