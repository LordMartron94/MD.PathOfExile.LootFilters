import math
from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem


class LogScaledRarityCalculator:
    """
    Assigns rarity tiers based on logarithmically scaled listing counts:
    1 = ultra common (highest counts), 12 = ultra rare (lowest counts).
    """
    def calculate(self, items: List[GameItem]) -> None:
        if not items:
            return

        # Compute log-scaled counts to compress heavy-tail distribution
        log_counts = [math.log1p(item.listing_count) for item in items]
        min_log, max_log = min(log_counts), max(log_counts)

        # If all counts equal, default to common
        if max_log == min_log:
            for item in items:
                item.rarity = 1
            return

        # Normalize log counts to [0,1] and invert for rarity
        for item, lc in zip(items, log_counts):
            normalized = (lc - min_log) / (max_log - min_log)
            # Invert: high listing_count => normalized ~1 => rarity ~1
            item.rarity = int((1 - normalized) * 11) + 1
