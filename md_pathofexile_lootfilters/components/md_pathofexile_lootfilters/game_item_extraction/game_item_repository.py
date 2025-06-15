from pathlib import Path
from typing import List, Dict, Tuple

import pandas as pd

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import DATA_DIR
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.ninja_client import \
    PoeNinjaClient

class GameItemRepository:
    """
    Responsible for fetching, validating, and mapping GameItem instances
    from multiple leagues using a weighted aggregation strategy.
    """
    def __init__(
            self,
            logger: HoornLogger,
            client: PoeNinjaClient,
            valid_bases: List[str],
            league_weights: Dict[str, float],
            item_types: Dict[Path, List[str]],
    ):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._client = client
        self._valid_bases = set(valid_bases)
        # league_weights maps league name to its weight for aggregation
        self._league_weights = league_weights
        self._leagues = list(league_weights.keys())
        self._item_types = item_types

        self._logger.info(
            f"Using leagues with weights: {self._league_weights}", separator=self._separator
        )

    def get_all_game_items(self) -> Dict[Path, List[GameItem]]:
        self._logger.debug(
            f"Loading game items for leagues {self._leagues}", separator=self._separator
        )
        return {
            path: self._load_items_for_path(path, types)
            for path, types in self._item_types.items()
        }

    def _load_items_for_path(
            self, path: Path, types: List[str]
    ) -> List[GameItem]:
        tagged = self._fetch_lines_by_league_and_type(types)
        aggregated = self._aggregate_stats(tagged)
        # Save aggregated stats to CSV for inspection
        df_agg = pd.DataFrame.from_records(list(aggregated.values()))
        csv_path = DATA_DIR / f"{path.name}_aggregated.csv"
        df_agg.to_csv(csv_path, index=False)
        self._logger.info(
            f"Saved aggregated stats to {csv_path}", separator=self._separator
        )

        valid_stats = self._filter_valid_aggregated(aggregated)
        # Save filtered stats to CSV as well
        df_valid = pd.DataFrame.from_records(valid_stats)
        csv_valid = DATA_DIR / f"{path.name}_valid_stats.csv"
        df_valid.to_csv(csv_valid, index=False)
        self._logger.info(
            f"Saved filtered stats to {csv_valid}", separator=self._separator
        )

        items = self._map_aggregated_to_items(valid_stats)

        self._logger.info(
            f"{path.name}: {len(items)} aggregated items from leagues", separator=self._separator
        )
        return items

    def _fetch_lines_by_league_and_type(
            self, types: List[str]
    ) -> List[Tuple[str, dict]]:
        collected: List[Tuple[str, dict]] = []
        for league in self._leagues:
            for t in types:
                data = self._client.fetch_game_items(league, t)
                lines = data.get("lines", [])
                self._logger.trace(
                    f"[{league}] fetched {len(lines)} lines for '{t}'",
                    separator=self._separator,
                )
                collected.extend((league, l) for l in lines)
        return collected

    def _aggregate_stats(
            self, tagged_lines: List[Tuple[str, dict]]
    ) -> Dict[Tuple[str, str], dict]:
        """
        Aggregate listing and count stats using league weights.
        """
        agg: Dict[Tuple[str, str], dict] = {}
        for league, line in tagged_lines:
            name = line.get("name", "")
            base = line.get("baseType", "")
            key = (name, base)
            weight = self._league_weights.get(league, 0)
            stats = agg.setdefault(key, {
                "name": name,
                "baseType": base,
                "weighted_listings": 0.0,
                "total_listings": 0,
                "max_listings": 0,
                "total_count": 0,
                "leagues_seen": set(),
            })
            lc = line.get("listingCount", 0)
            cnt = line.get("count", 0)
            stats["weighted_listings"] += lc * weight
            stats["total_listings"] += lc
            stats["max_listings"] = max(stats["max_listings"], lc)
            stats["total_count"] += cnt
            stats["leagues_seen"].add(league)

        # Compute average weighted listing per league seen
        for stats in agg.values():
            seen = stats["leagues_seen"]
            stats["avg_weighted_listings"] = (
                stats["weighted_listings"] / len(seen) if seen else 0.0
            )
        return agg

    def _filter_valid_aggregated(
            self, aggregated: Dict[Tuple[str, str], dict]
    ) -> List[dict]:
        """
        Keep only entries whose baseType is valid, logging filter stats.
        """
        total = len(aggregated)
        valid = [v for v in aggregated.values() if v["baseType"] in self._valid_bases]
        excluded = total - len(valid)
        passed_pct = (len(valid) / total * 100) if total else 0.0
        excluded_pct = (excluded / total * 100) if total else 0.0
        self._logger.info(
            f"Aggregated filter: {len(valid)} passed, {excluded} excluded "
            f"(passed={passed_pct:.4f}%; excluded={excluded_pct:.4f}%)",
            separator=self._separator,
        )
        return valid

    @staticmethod
    def _map_aggregated_to_items(stats_list: List[dict]) -> List[GameItem]:
        """
        Map aggregated stats to GameItem, using weighted listings for rarity.
        """
        items: List[GameItem] = []
        for s in stats_list:
            item = GameItem(
                name=s["name"],
                base_type=s["baseType"],
                listing_count=int(s["avg_weighted_listings"]),
                count=s["total_count"],
            )
            items.append(item)
        return items
