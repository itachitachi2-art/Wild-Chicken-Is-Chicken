public sealed class WildChickenIsChickenMod : IModApi
{
    public void InitMod(Mod mod)
    {
        ModEvents.WorldShuttingDown.RegisterHandler(OnWorldShuttingDown);
        Log.Out("[WildChickenIsChicken] v0.1.3-test1 loaded; rebuilt for 7DTD v3.3 API (holdingEntity property); in-game validation pending.");
    }

    private static void OnWorldShuttingDown(ref ModEvents.SWorldShuttingDownData data)
    {
        var manager = GameManager.Instance;
        if (manager == null) return;
        var feedback = manager.GetComponent<WCICButcherFeedback>();
        if (feedback != null) feedback.FlushAccepted();
    }
}
