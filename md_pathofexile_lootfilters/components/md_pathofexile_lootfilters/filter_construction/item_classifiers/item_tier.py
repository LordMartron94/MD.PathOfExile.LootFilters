import enum
from typing import Optional


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

def get_new_tier(
        old_tier: ItemTier,
        rarity: Optional[str] = None,
        bump: Optional[int] = None
) -> ItemTier:
    """
    Calculate a new ItemTier by moving up or down the tier ladder.
    By default, bump is determined by rarity:
      Normal -> -2, Magic -> -1, Rare -> 0.
    Clients can override bump directly by supplying the `bump` parameter.
    """
    tier_order = [
        t for t in reversed(list(ItemTier))
        if t is not ItemTier.NoTier
    ]

    if bump is None:
        rarity_bumps = {"Normal": -2, "Magic": -1, "Rare": 0}
        bump = rarity_bumps.get(rarity, 0)

    try:
        idx = tier_order.index(old_tier)
    except ValueError:
        return ItemTier.NoTier

    new_idx = min(max(idx + bump, 0), len(tier_order) - 1)
    return tier_order[new_idx]
