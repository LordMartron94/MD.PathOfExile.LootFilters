from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.model.unique_item import \
    UniqueItem


class PercentileRarityCalculator:
    """
    Divides the distribution of listing counts into 12 bands:
    1 = ultra common, 12 = ultra rare.
    """
    def calculate(self, items: List[UniqueItem]) -> None:
        if not items:
            return
        counts = [item.listing_count for item in items]
        # Sort descending: highest count => most common
        sorted_counts = sorted(counts, reverse=True)
        n = len(sorted_counts) - 1
        if n <= 0:
            for item in items:
                item.rarity = 1
            return
        # Map each count to a rarity bucket
        rarity_map = {count: int(idx / n * 11) + 1 for idx, count in enumerate(sorted_counts)}
        for item in items:
            item.rarity = rarity_map.get(item.listing_count, 1)
