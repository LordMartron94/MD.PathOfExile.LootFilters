from pathlib import Path
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.ninja_client import \
    PoeNinjaClient


class GameItemRepository:
    """
    Repository for loading unique GameItem instances per league, grouped by output path.

    Responsibilities:
        - Fetch raw unique-item data from PoeNinjaClient
        - Transform raw data into GameItem models
        - Group items by configured output Path
    """

    def __init__(
            self,
            client: PoeNinjaClient,
            league: str,
            item_types: Dict[Path, List[str]]
    ) -> None:
        self._client = client
        self._league = league
        self._item_types = item_types

    def get_all_game_items(self) -> Dict[Path, List[GameItem]]:
        """
        Fetch and group all GameItems by output Path.
        """
        result: Dict[Path, List[GameItem]] = {}
        for output_path, types in self._item_types.items():
            result[output_path] = self._load_items_for_path(types)
        return result

    def _load_items_for_path(self, types: List[str]) -> List[GameItem]:
        """
        Fetch and map GameItems for the given list of unique item types.
        """
        items: List[GameItem] = []
        for item_type in types:
            lines = self._fetch_lines(item_type)
            items.extend(self._map_to_game_items(lines))
        return items

    def _fetch_lines(self, item_type: str) -> List[dict]:
        """
        Fetch raw data for a single unique-item type and return its 'lines'.
        """
        data = self._client.fetch_unique_items(self._league, item_type)
        return data.get("lines", [])

    @staticmethod
    def _map_to_game_items(lines: List[dict]) -> List[GameItem]:
        """
        Convert raw line dictionaries into GameItem instances.
        """
        return [
            GameItem(
                name=line["name"],
                base_type=line.get("baseType", ""),
                listing_count=line.get("listingCount", 0),
                count=line.get("count", 0)
            )
            for line in lines
        ]
