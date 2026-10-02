using UnityEngine;

// Uses the game's item-action extension point; no Harmony patches are installed.
public sealed class ItemActionWCICButcherChicken : ItemAction
{
    private const string SourceName = "wildChicken";
    private const string ResultName = "wcicButcheredChicken";
    private const int FeatherCount = 23; // animalChicken's vanilla base harvest.

    private sealed class ButcherData : ItemActionData
    {
        public bool Armed;
        public bool Busy;
        public ButcherData(ItemInventoryData inventoryData, int actionIndex)
            : base(inventoryData, actionIndex) { }
    }

    public override ItemActionData CreateModifierData(ItemInventoryData inventoryData, int actionIndex)
    {
        return new ButcherData(inventoryData, actionIndex);
    }

    public override void StopHolding(ItemActionData actionData)
    {
        var data = actionData as ButcherData;
        if (data != null) data.Armed = false;
        base.StopHolding(actionData);
    }

    // Secondary-action press followed by release is an explicit, single-use choice.
    public override void ExecuteAction(ItemActionData actionData, bool released)
    {
        var data = actionData as ButcherData;
        if (data == null || data.Busy) return;
        if (!released)
        {
            data.Armed = true;
            return;
        }
        if (!data.Armed) return;
        data.Armed = false;

        var inventoryData = data.invData;
        var player = inventoryData.holdingEntity as EntityPlayerLocal;
        if (player == null || player.IsDead()) return;
        // OnPlacedAsCatalyst uses the primary player internally. Never call it for
        // a different actor, or on a dedicated server's remote actor.
        var manager = GameManager.Instance;
        if (manager == null || manager.World == null ||
            !object.ReferenceEquals(manager.World.GetPrimaryPlayer(), player)) return;

        var inventory = player.inventory;
        int slot = inventory.holdingItemIdx;
        if (slot != inventoryData.slotIdx) return;
        var source = inventory.GetItem(slot);
        if (!object.ReferenceEquals(source, inventoryData.itemStack) || source.count != 1) return;
        var heldChicken = source.itemValue.ItemClass as ItemClassWildChicken;
        if (heldChicken == null || heldChicken.GetItemName() != SourceName) return;

        // Resolve and allocate the result BEFORE altering the live chicken.
        var result = ItemClass.GetItem(ResultName, false);
        if (result == null || result.type == 0 || result.ItemClass == null) return;
        var replacement = new ItemStack(result, 1);
        var featherItem = ItemClass.GetItem("resourceFeather", false);
        if (featherItem == null || featherItem.type == 0 || featherItem.ItemClass == null) return;
        var feathers = new ItemStack(featherItem, FeatherCount);
        var ui = LocalPlayerUI.GetUIForPlayer(player);
        if (ui == null || ui.xui == null || ui.xui.PlayerInventory == null) return;
        if (Time.time - data.lastUseTime < Delay) return;

        data.Busy = true;
        try
        {
            data.lastUseTime = Time.time;
            // The same cleanup the vanilla collector uses: set the held-slot CVar
            // to -1, remove the stress buff, and remove the mount listener.
            // This makes StopHolding skip DropEntity when SetItem clears the slot.
            heldChicken.OnPlacedAsCatalyst(inventoryData);
            player.SetCVar(".UseAltEntity", 0f);
            // Replace the occupied toolbelt slot directly: no free bag slot is
            // needed, no loose live entity is spawned, and no output is duplicated.
            inventory.SetItem(slot, replacement);
            // Use the same add/fallback pattern as vanilla ItemActionEat.
            // AddItem mutates this stack to the remainder after partial insertion.
            if (!ui.xui.PlayerInventory.AddItem(feathers) && feathers.count > 0)
            {
                manager.ItemDropServer(feathers, player.GetPosition(), Vector3.zero, -1, 60f, false);
            }
        }
        finally
        {
            data.Busy = false;
        }
    }
}
