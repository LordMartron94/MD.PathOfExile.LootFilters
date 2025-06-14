from typing import Protocol, List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.model.unique_item import \
    UniqueItem


class IRarityCalculator(Protocol):
    def calculate(self, items: List[UniqueItem]) -> None:
        """Assigns rarity (1–12) to each UniqueItem based on listing_count distribution."""
        ...
