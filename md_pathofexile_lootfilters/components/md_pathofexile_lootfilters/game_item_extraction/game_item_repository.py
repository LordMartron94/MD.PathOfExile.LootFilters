from pathlib import Path
from typing import List, Dict, Tuple

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.ninja_client import \
    PoeNinjaClient


class GameItemRepository:
    """
    Responsible for fetching, validating, and mapping GameItem instances per league.
    """
    def __init__(
            self,
            logger: HoornLogger,
            client: PoeNinjaClient,
            valid_bases: List[str],
            league: str,
            item_types: Dict[Path, List[str]]
    ):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._client = client
        self._valid_bases = valid_bases
        self._league = league
        self._item_types = item_types
        self._valid_base_types = self._load_valid_base_types()

    def _load_valid_base_types(self) -> set[str]:
        types = set(self._valid_bases)
        self._logger.info(f"Valid base types: {len(types)}", separator=self._separator)
        return types

    def get_all_game_items(self) -> Dict[Path, List[GameItem]]:
        self._logger.debug(f"Loading game items for league '{self._league}'", separator=self._separator)
        result = {
            path: self._load_items(path, types)
            for path, types in self._item_types.items()
        }
        self._logger.info(f"Loaded items for {len(result)} paths", separator=self._separator)
        return result

    def _load_items(self, path: Path, types: List[str]) -> List[GameItem]:
        lines = self._fetch_lines(types)
        valid, excluded = self._filter_valid(lines)
        items = self._map_to_items(valid)
        passed_pct = (len(valid) / len(lines) * 100) if lines else 0.0
        excluded_pct = (excluded / len(lines) * 100) if lines else 0.0
        self._logger.info(
            f"{path.name}: {len(valid)} passed, {excluded} excluded (passed={passed_pct:.4f}%; excluded={excluded_pct:.4f}%)",
            separator=self._separator
        )
        return items

    def _fetch_lines(self, types: List[str]) -> List[dict]:
        all_lines: List[dict] = []
        for t in types:
            data = self._client.fetch_game_items(self._league, t)
            lines = data.get("lines", [])
            self._logger.trace(f"Fetched {len(lines)} lines for '{t}'", separator=self._separator)
            all_lines.extend(lines)
        return all_lines

    def _filter_valid(self, lines: List[dict]) -> Tuple[List[dict], int]:
        valid = [l for l in lines if l.get("baseType", "") in self._valid_base_types]
        return valid, len(lines) - len(valid)

    @staticmethod
    def _map_to_items(lines: List[dict]) -> List[GameItem]:
        return [
            GameItem(
                name=l["name"],
                base_type=l.get("baseType", ""),
                listing_count=l.get("listingCount", 0),
                count=l.get("count", 0)
            )
            for l in lines
        ]
