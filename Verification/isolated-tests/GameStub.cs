using System;
using System.Collections.Generic;
namespace UnityEngine { public static class Time { public static float time = 100f; } }
public class EntityAlive { }
public class EntityPlayerLocal : EntityAlive {
    public Inventory inventory = new Inventory();
    public bool Dead;
    public bool IsDead() { return Dead; }
    public void SetCVar(string name, float value) { }
}
public class ItemActionData {
    public ItemInventoryData invData;
    public float lastUseTime;
    public ItemActionData(ItemInventoryData data, int actionIndex) { invData = data; }
}
public class ItemAction {
    public float Delay = .5f;
    public virtual ItemActionData CreateModifierData(ItemInventoryData d, int i) { return null; }
    public virtual void StopHolding(ItemActionData d) { }
    public virtual void ExecuteAction(ItemActionData d, bool released) { }
}
public class ItemInventoryData {
#if PROPERTY_API
    public EntityAlive holdingEntity { get; private set; }
#else
    public EntityAlive holdingEntity;
#endif
    public int slotIdx;
    public ItemStack itemStack;
    public ItemInventoryData(EntityAlive actor, ItemStack item) { holdingEntity = actor; itemStack = item; }
}
public class ItemValue {
    public int type;
    public ItemClass ItemClass;
    public ItemValue(ItemClass item, int id) { ItemClass = item; type = id; }
}
public class ItemStack {
    public static ItemStack Empty = new ItemStack(null, 0);
    public ItemValue itemValue;
    public int count;
    public ItemStack(ItemValue item, int n) { itemValue = item; count = n; }
    public ItemStack Clone() { return new ItemStack(itemValue, count); }
}
public class ItemClass {
    public string Name;
    public string GetItemName() { return Name; }
    public static ItemValue GetItem(string name, bool unused) { return new ItemValue(new ItemClass { Name = name }, 1); }
}
public class ItemClassWildChicken : ItemClass {
    public int CleanupCalls;
    public void OnPlacedAsCatalyst(ItemInventoryData data) { ++CleanupCalls; }
}
public class Inventory {
    public int holdingItemIdx;
    public ItemStack Stack;
    public int Writes;
    public ItemStack GetItem(int slot) { return Stack; }
    public void SetItem(int slot, ItemStack item) { Stack = item; ++Writes; }
}
public class World {
    public EntityPlayerLocal Player;
    public EntityPlayerLocal GetPrimaryPlayer() { return Player; }
}
public class GameManager {
    public static GameManager Instance;
    public World World;
}
public class XUi { public object PlayerInventory = new object(); }
public class LocalPlayerUI {
    public static LocalPlayerUI Current = new LocalPlayerUI();
    public XUi xui = new XUi();
    public static LocalPlayerUI GetUIForPlayer(EntityPlayerLocal player) { return Current; }
}
public class WCICButcherFeedback {
    public sealed class Pending { public ItemStack Chicken; public ItemStack Feathers; }
    public static WCICButcherFeedback Instance = new WCICButcherFeedback();
    public List<Pending> Accepted = new List<Pending>();
    public static WCICButcherFeedback GetOrCreate(GameManager manager) { return Instance; }
    public Pending Prepare(GameManager manager, EntityPlayerLocal player, int slot, ItemStack chicken, ItemStack feathers) {
        return new Pending { Chicken = chicken, Feathers = feathers };
    }
    public void Begin(Pending pending) { Accepted.Add(pending); }
}
public static class GameHarness {
    public static ItemInventoryData Prepare(bool primary, int count, bool dead, bool ui) {
        var player = new EntityPlayerLocal { Dead = dead };
        var chicken = new ItemClassWildChicken { Name = "wildChicken" };
        var stack = new ItemStack(new ItemValue(chicken, 1), count);
        player.inventory.Stack = stack;
        GameManager.Instance = new GameManager { World = new World { Player = primary ? player : new EntityPlayerLocal() } };
        LocalPlayerUI.Current = ui ? new LocalPlayerUI() : null;
        WCICButcherFeedback.Instance = new WCICButcherFeedback();
        return new ItemInventoryData(player, stack);
    }
    public static int Accepted { get { return WCICButcherFeedback.Instance.Accepted.Count; } }
}
