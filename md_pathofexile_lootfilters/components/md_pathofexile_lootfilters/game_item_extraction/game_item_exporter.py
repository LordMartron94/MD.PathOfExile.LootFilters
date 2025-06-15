from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import GameItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.rarity_calculation.rarity_calculator_interface import IRarityCalculator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.game_item_repository import GameItemRepository
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.utils.duplicate_aggregator import DuplicateAggregator


class GameItemExporter:
    """
    High-level orchestration: load, dedupe variants across all items,
    calculate rarity globally, and write per-path results.
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
        # Load all raw items grouped by output path
        all_items: Dict[Path, List[GameItem]] = self._repository.get_all_game_items()

        # Flatten and dedupe across the entire dataset
        all_raw_items: List[GameItem] = [item for sublist in all_items.values() for item in sublist]
        deduped_items: List[GameItem] = self._aggregator.aggregate(all_raw_items)

        # Perform a single global rarity calculation
        self._calculator.calculate(deduped_items)

        # Build a lookup map from (Base Type, Item Name) to deduped GameItem
        item_map: Dict[Tuple[str, str], GameItem] = {
            (item.base_type, item.name): item for item in deduped_items
        }

        # Write out per-path CSVs using the globally-calculated rarities
        for output_path, raw_items in all_items.items():
            # Identify unique keys for this path
            keys = {(itm.base_type, itm.name) for itm in raw_items}
            items = [item_map[key] for key in keys if key in item_map]

            df = pd.DataFrame([{
                "Base Type":  game_item.base_type,
                "Item Name":  game_item.name,
                "Rarity":     game_item.rarity,
                "List Count": game_item.listing_count,
                "Count":      game_item.count
            } for game_item in items])

            self._logger.info(
                f"Inserted {len(df)} game items!",
                separator=self._separator
            )

            df.to_csv(output_path, index=False)
