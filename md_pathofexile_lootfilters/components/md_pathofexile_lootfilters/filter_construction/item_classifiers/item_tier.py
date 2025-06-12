import enum


class ItemTier(enum.Enum):
    GodTier1 = "God-Tier 1"
    GodTier2 = "God-Tier 2"
    GodTier3 = "God-Tier 3"
    HighTier1 = "High-Tier 1"
    HighTier2 = "High-Tier 2"
    HighTier3 = "High-Tier 3"
    MidTier1 = "Mid-Tier 1"
    MidTier2 = "Mid-Tier 2"
    MidTier3 = "Mid-Tier 3"
    LowTier1 = "Low-Tier 1"
    LowTier2 = "Low-Tier 2"
    LowTier3 = "Low-Tier 3"
    NoTier = "NoTier"

def get_new_tier(old_tier: ItemTier, rarity: str):
    # 2) define the full tier‐ladder to climb
    tier_order = [
        ItemTier.LowTier1, ItemTier.LowTier2, ItemTier.LowTier3,
        ItemTier.MidTier1, ItemTier.MidTier2, ItemTier.MidTier3,
        ItemTier.HighTier1, ItemTier.HighTier2, ItemTier.HighTier3,
        ItemTier.GodTier1, ItemTier.GodTier2,  ItemTier.GodTier3,
    ]

    # 3) how many steps to climb for each rarity
    bump = {"Normal": 0, "Magic": 1, "Rare": 2}[rarity]

    idx = tier_order.index(old_tier)
    final_tier = tier_order[min(idx + bump, len(tier_order) - 1)]

    return final_tier
