public sealed class WildChickenIsChickenMod : IModApi
{
    public void InitMod(Mod mod)
    {
        ModEvents.WorldShuttingDown.RegisterHandler(OnWorldShuttingDown);
        Log.Out("[WildChickenIsChicken] v0.1.2 loaded; decorative slaughter bar and chicken sound enabled.");
    }

    private static void OnWorldShuttingDown(ref ModEvents.SWorldShuttingDownData data)
    {
        var manager = GameManager.Instance;
        if (manager == null) return;
        var feedback = manager.GetComponent<WCICButcherFeedback>();
        if (feedback != null) feedback.FlushAccepted();
    }
}
