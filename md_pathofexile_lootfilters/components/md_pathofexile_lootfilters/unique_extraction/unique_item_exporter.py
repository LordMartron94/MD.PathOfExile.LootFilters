from pathlib import Path

import pandas as pd

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.rarity_calculation.rarity_calculator_interface import \
    IRarityCalculator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.unique_extraction.unique_item_repository import \
    UniqueItemRepository


class UniqueItemExporter:
    """
    High-level orchestration: load, calculate rarity, and write results.
    """
    def __init__(
            self,
            logger: HoornLogger,
            repository: UniqueItemRepository,
            calculator: IRarityCalculator
    ):
        self._logger = logger
        self._separator: str = self.__class__.__name__
        self._repository = repository
        self._calculator = calculator

    def export(self, output_path: Path) -> None:
        items = self._repository.get_all_unique_items()
        self._calculator.calculate(items)

        # Build DataFrame
        df = pd.DataFrame([{
            "Base Type": item.base_type,
            "Unique Name": item.name,
            "Rarity": item.rarity,
            "List Count": item.listing_count,
            "Count": item.count
        } for item in items])

        # Group by Base Type and Unique Name, aggregate medians for numeric fields
        grouped = (
            df.groupby(["Base Type", "Unique Name"], as_index=False)
            .agg({
                "Rarity": "median",
                "List Count": "median",
                "Count": "median"
            })
        )

        self._logger.info(
            f"Inserted {len(grouped)} unique items!",
            separator=self._separator
        )

        df.to_csv(output_path, index=False)
