from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.model.unique_item import \
    UniqueItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.ninja_client import \
    PoeNinjaClient


class UniqueItemRepository:
    """
    Loads all unique items for a league by fetching each "Unique*" category.
    """
    def __init__(self, client: PoeNinjaClient, league: str):
        self._client = client
        self._league = league
        self._item_types = [
            "UniqueArmour", "UniqueWeapon", "UniqueAccessory",
            "UniqueJewel", "UniqueFlask", "UniqueMap", "UniqueRelic"
        ]

    def get_all_unique_items(self) -> List[UniqueItem]:
        items: List[UniqueItem] = []
        for item_type in self._item_types:
            data = self._client.fetch_unique_items(self._league, item_type)
            lines = data.get("lines", [])
            for line in lines:
                items.append(UniqueItem(
                    name=line["name"],
                    base_type=line.get("baseType", ""),
                    listing_count=line.get("listingCount", 0),
                    count=line.get("count", 0)
                ))
        return items
