import enum
import math
from typing import Tuple


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

# ----- Configuration constants -----
_MIN_INPUT: float         = 1.0
_MAX_INPUT: float         = 6.0
_NUM_TIERS: int           = 12
_USEFULNESS_WEIGHT: float = 0.7
_RARITY_WEIGHT: float     = 0.3
_PRIMARY_NAMES: Tuple[str, ...] = ("LowTier", "MidTier", "HighTier", "GodTier")
_ORDERED_TIERS: Tuple[ItemTier, ...] = tuple(
    getattr(ItemTier, f"{name}{sub}")
    for name in _PRIMARY_NAMES
    for sub in (1, 2, 3)
)


def get_tier_from_rarity_and_use(rarity: float, usefulness: float) -> ItemTier:
    """
    Maps rarity & usefulness (1.0–6.0 each) to one of 12 ItemTier values,
    using a 70/30 weighted sum plus equal-interval classification.
    """
    # 1) Validate inputs
    if not (_MIN_INPUT <= rarity <= _MAX_INPUT and _MIN_INPUT <= usefulness <= _MAX_INPUT):
        raise ValueError(
            f"rarity/usefulness must be between {_MIN_INPUT} and {_MAX_INPUT}; "
            f"got rarity={rarity}, usefulness={usefulness}"
        )

    # 2) Weighted-sum score
    score = _USEFULNESS_WEIGHT * usefulness + _RARITY_WEIGHT * rarity

    # 3) Normalize score into [0, 1), then scale to tier-index [0, NUM_TIERS]
    span = _MAX_INPUT - _MIN_INPUT
    normalized = (score - _MIN_INPUT) / span
    raw_idx = math.floor(normalized * _NUM_TIERS)
    idx = max(0, min(raw_idx, _NUM_TIERS - 1))

    # 4) Primary tier (0–3) and sub-index (0–2)
    primary_idx = idx // 3
    sub_idx     = idx % 3
    sub_tier    = 3 - sub_idx

    # 5) Lookup by NAME, not by VALUE
    tier_key = f"{_PRIMARY_NAMES[primary_idx]}{sub_tier}"
    return getattr(ItemTier, tier_key)

def get_tier_from_rarity(rarity: float) -> ItemTier:
    """
    Maps rarity (1.0–12.0) to one of 12 ItemTier values
    """
    # 1) Validate inputs
    if not (_MIN_INPUT <= rarity <= 12.0):
        raise ValueError(
            f"rarity must be between {_MIN_INPUT} and {_MAX_INPUT}; "
            f"got rarity={rarity}"
        )

    # 2) Normalize score into [0, 1), then scale to tier-index [0, NUM_TIERS]
    span = _MAX_INPUT - _MIN_INPUT
    normalized = (rarity - _MIN_INPUT) / span
    raw_idx = math.floor(normalized * _NUM_TIERS)
    idx = max(0, min(raw_idx, _NUM_TIERS - 1))

    # 3) Primary tier (0–3) and sub-index (0–2)
    primary_idx = idx // 3
    sub_idx     = idx % 3
    sub_tier    = 3 - sub_idx

    # 4) Lookup by NAME, not by VALUE
    tier_key = f"{_PRIMARY_NAMES[primary_idx]}{sub_tier}"
    return getattr(ItemTier, tier_key)

def parse_tier_value(tier_value: str) -> ItemTier:
    """
    Parses a tier’s string value into its corresponding ItemTier member.

    :param tier_value: The exact string value of one of the ItemTier members.
    :return: The matching ItemTier member.
    :raises ValueError: If tier_value doesn’t match any ItemTier.value.
    """
    try:
        return ItemTier(tier_value)
    except ValueError as err:
        valid = [t.value for t in ItemTier]
        raise ValueError(
            f"Invalid tier value {tier_value!r}. "
            f"Expected one of: {valid}"
        ) from err

def bump_tier(current: ItemTier, bump: int) -> ItemTier:
    """
    Returns a new ItemTier by moving `bump` steps in the ordered tiers list.
    Positive bump → higher; negative bump → lower.
    Ends are saturated (i.e. clamped to lowest/highest tier).

    :param current: The starting ItemTier (must not be NoTier).
    :param bump:   Number of steps to move (can be negative).
    :return:       The resulting ItemTier.
    :raises ValueError: If `current` is NoTier.
    """
    if current is ItemTier.NoTier:
        raise ValueError("Cannot bump NoTier")

    idx = _ORDERED_TIERS.index(current) + bump

    idx = max(0, min(idx, len(_ORDERED_TIERS) - 1))
    return _ORDERED_TIERS[idx]
