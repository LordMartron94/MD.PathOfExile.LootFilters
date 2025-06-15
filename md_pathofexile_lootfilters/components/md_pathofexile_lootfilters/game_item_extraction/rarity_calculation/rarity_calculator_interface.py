from typing import Protocol, List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem


class IRarityCalculator(Protocol):
    def calculate(self, items: List[GameItem]) -> None:
        """Assigns rarity (1–12) to each UniqueItem based on listing_count distribution."""
        ...
