using System;
using System.Collections.Generic;
using UnityEngine;

// Presentation runs on the game manager, not on the held item. Changing items
// or releasing the button cannot cancel an already accepted chicken.
public sealed class WCICButcherFeedback : MonoBehaviour
{
    private const float Duration = 2f;
    private readonly List<PendingChicken> pending = new List<PendingChicken>();

    public sealed class PendingChicken
    {
        public GameManager Manager;
        public World World;
        public EntityPlayerLocal Player;
        public int Slot;
        public ItemStack Chicken;
        public ItemStack Feathers;
        public float Started;
        public bool SoundAttempted;
        public bool ChickenDelivered;
        public bool FeathersDelivered;
        public bool ErrorReported;
    }

    public static WCICButcherFeedback GetOrCreate(GameManager manager)
    {
        var feedback = manager.GetComponent<WCICButcherFeedback>();
        if (feedback == null) feedback = manager.gameObject.AddComponent<WCICButcherFeedback>();
        return feedback;
    }

    // Reserve list storage before the source item is consumed.
    public PendingChicken Prepare(GameManager manager, EntityPlayerLocal player,
        int slot, ItemStack chicken, ItemStack feathers)
    {
        if (pending.Capacity == pending.Count) pending.Capacity = pending.Count + 4;
        return new PendingChicken {
            Manager = manager, World = manager.World, Player = player,
            Slot = slot, Chicken = chicken, Feathers = feathers
        };
    }

    public void Begin(PendingChicken chicken)
    {
        chicken.Started = Time.unscaledTime;
        pending.Add(chicken);
    }

    private static bool IsSameWorld(PendingChicken chicken)
    {
        return chicken.Manager != null && chicken.Player != null &&
            object.ReferenceEquals(chicken.Manager.World, chicken.World) &&
            object.ReferenceEquals(chicken.World.GetPrimaryPlayer(), chicken.Player);
    }

    private void Update()
    {
        for (int i = pending.Count - 1; i >= 0; --i)
        {
            var chicken = pending[i];
            if (!IsSameWorld(chicken))
            {
                // Never deliver an old world's items to a new player/session.
                pending.RemoveAt(i);
                continue;
            }
            if (Time.unscaledTime - chicken.Started < Duration) continue;
            Complete(chicken);
            if (chicken.ChickenDelivered && chicken.FeathersDelivered) pending.RemoveAt(i);
        }
    }

    private static void Complete(PendingChicken chicken)
    {
        // This ordering is intentional: request the cluck BEFORE either reward.
        if (!chicken.SoundAttempted)
        {
            chicken.SoundAttempted = true;
            try { Audio.Manager.Play(chicken.Player, "chickendeath", 1f, false); }
            catch (Exception error) { Log.Warning("[WildChickenIsChicken] Chicken sound failed: " + error.Message); }
        }
        try
        {
            var ui = LocalPlayerUI.GetUIForPlayer(chicken.Player);
            if (ui == null || ui.xui == null || ui.xui.PlayerInventory == null) return;
            if (!chicken.ChickenDelivered)
            {
                // Preserve the original slot if still empty; never overwrite a
                // different item moved there during this decorative animation.
                if (chicken.Player.inventory.GetItem(chicken.Slot).IsEmpty())
                    chicken.Player.inventory.SetItem(chicken.Slot, chicken.Chicken);
                else
                    AddOrDrop(chicken, chicken.Chicken, ui);
                chicken.ChickenDelivered = true;
            }
            if (!chicken.FeathersDelivered)
            {
                AddOrDrop(chicken, chicken.Feathers, ui);
                chicken.FeathersDelivered = true;
            }
        }
        catch (Exception error)
        {
            // Keep undelivered remainders for the next frame, without replaying
            // the sound or delivering the already completed reward again.
            if (!chicken.ErrorReported)
            {
                chicken.ErrorReported = true;
                Log.Warning("[WildChickenIsChicken] Reward delivery will retry: " + error.Message);
            }
        }
    }

    private static void AddOrDrop(PendingChicken chicken, ItemStack stack, LocalPlayerUI ui)
    {
        if (stack.count <= 0) return;
        if (!ui.xui.PlayerInventory.AddItem(stack) && stack.count > 0)
            chicken.Manager.ItemDropServer(stack, chicken.Player.GetPosition(), Vector3.zero, -1, 60f, false);
    }

    private void OnApplicationQuit()
    {
        // Flush accepted rewards before shutdown instead of requiring the user
        // to remain in-game solely for a decorative timer.
        FlushAccepted();
    }

    public void FlushAccepted()
    {
        foreach (var chicken in pending)
            if (IsSameWorld(chicken)) Complete(chicken);
        pending.RemoveAll(delegate(PendingChicken chicken) {
            return chicken.ChickenDelivered && chicken.FeathersDelivered;
        });
    }

    private void OnGUI()
    {
        if (Event.current.type != EventType.Repaint) return;
        PendingChicken visible = null;
        foreach (var chicken in pending)
            if (IsSameWorld(chicken) && Time.unscaledTime - chicken.Started < Duration)
            { visible = chicken; break; }
        if (visible == null) return;

        float scale = Mathf.Clamp(Screen.height / 1080f, 0.65f, 2f);
        float width = 300f * scale;
        float height = 14f * scale;
        float x = (Screen.width - width) / 2f;
        float y = Screen.height * 0.72f;
        float progress = Mathf.Clamp01((Time.unscaledTime - visible.Started) / Duration);
        Color previous = GUI.color;
        try
        {
            GUI.color = Color.white;
            var style = new GUIStyle(GUI.skin.label);
            style.alignment = TextAnchor.MiddleCenter;
            style.fontSize = (int)(18f * scale);
            GUI.Label(new Rect(x, y - 30f * scale, width, 26f * scale),
                Localization.Get("wcicButchering"), style);
            GUI.color = new Color(0f, 0f, 0f, 0.8f);
            GUI.DrawTexture(new Rect(x - 2f, y - 2f, width + 4f, height + 4f), Texture2D.whiteTexture);
            GUI.color = new Color(0.2f, 0.2f, 0.2f, 0.9f);
            GUI.DrawTexture(new Rect(x, y, width, height), Texture2D.whiteTexture);
            GUI.color = new Color(0.9f, 0.72f, 0.28f, 1f);
            GUI.DrawTexture(new Rect(x, y, width * progress, height), Texture2D.whiteTexture);
        }
        finally { GUI.color = previous; }
    }
}
