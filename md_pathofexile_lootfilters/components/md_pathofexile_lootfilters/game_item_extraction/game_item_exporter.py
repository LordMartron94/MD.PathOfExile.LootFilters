from pathlib import Path
from typing import Dict, List

import pandas as pd
from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.game_item_repository import GameItemRepository
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import GameItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.rarity_calculation.rarity_calculator_interface import IRarityCalculator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.utils.duplicate_aggregator import DuplicateAggregator


class GameItemExporter:
    """
    Orchestrates loading, deduplication, rarity calculation per output path,
    and writing results for Path of Exile loot filters.
    """
    def __init__(
            self,
            logger: HoornLogger,
            repository: GameItemRepository,
            calculator: IRarityCalculator,
            aggregator: DuplicateAggregator = DuplicateAggregator()
    ) -> None:
        self._logger = logger
        self._separator: str = self.__class__.__name__
        self._repository = repository
        self._calculator = calculator
        self._aggregator = aggregator

    def export(self) -> None:
        items_by_path = self._load_and_dedupe_items()

        for output_path, items in items_by_path.items():
            self._calculate_rarity(items)
            df = self._build_dataframe(items)
            self._write_csv(df, output_path)

    def _load_and_dedupe_items(self) -> Dict[Path, List[GameItem]]:
        """Load all raw items, dedupe globally, and map deduped items back per path."""
        raw_groups = self._repository.get_all_game_items()
        all_raw = [item for group in raw_groups.values() for item in group]
        deduped = self._aggregator.aggregate(all_raw)
        lookup = {(itm.base_type, itm.name): itm for itm in deduped}
        return {
            path: [lookup[(i.base_type, i.name)] for i in items if (i.base_type, i.name) in lookup]
            for path, items in raw_groups.items()
        }

    def _calculate_rarity(self, items: List[GameItem]) -> None:
        """Run the rarity calculator on the list of items for a single path."""
        if items:
            self._calculator.calculate(items)

    def _build_dataframe(self, items: List[GameItem]) -> pd.DataFrame:
        """Construct a DataFrame from items with assigned rarities."""
        records = [
            {
                "Base Type": itm.base_type,
                "Item Name": itm.name,
                "Rarity": itm.rarity,
                "List Count": itm.listing_count,
                "Count": itm.count
            }
            for itm in items
        ]
        df = pd.DataFrame(records)
        self._logger.info(f"Inserted {len(df)} game items!", separator=self._separator)
        return df

    @staticmethod
    def _write_csv(df: pd.DataFrame, path: Path) -> None:
        """Write the DataFrame to a CSV at the given path."""
        df.to_csv(path, index=False)
