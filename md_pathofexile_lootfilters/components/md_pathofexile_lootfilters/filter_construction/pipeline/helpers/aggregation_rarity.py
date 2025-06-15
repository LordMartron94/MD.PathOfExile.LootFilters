from typing import Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.helpers.rarity_score_calculator import \
    RarityScoreCalculator


class BaseTypeRarityAggregator:
    def __init__(self, calculator: Optional[RarityScoreCalculator] = None) -> None:
        """
        Aggregate per-base-type rarity using a configurable RarityScoreCalculator.

        Attributes:
            calculator: An instance of RarityScoreCalculator used to compute blended rarity scores.
        """

        self._calculator = calculator or RarityScoreCalculator()

    def aggregate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute total counts and blended rarity score for each base type.

        Args:
            df: DataFrame with columns ['Base Type', 'Rarity', 'Count']

        Returns:
            DataFrame with columns ['Base Type', 'total_count', 'rarity_score']
        """
        # Copy to avoid mutating input
        df_copy = df.copy()

        records = []
        for base_type, group in df_copy.groupby('Base Type'):
            rarities = group['Rarity'].to_numpy()
            counts = group['Count'].to_numpy()
            total_count = int(counts.sum())
            rarity_score = self._calculator.compute_score(rarities, counts)

            records.append({
                'Base Type': base_type,
                'total_count': total_count,
                'rarity_score': rarity_score
            })

        return pd.DataFrame.from_records(records)
