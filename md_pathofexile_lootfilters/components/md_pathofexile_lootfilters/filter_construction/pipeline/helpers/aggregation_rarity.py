from typing import Sequence

import numpy as np
import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.rarity_calculation.gaussian_mixture_rarity_calculator import \
    GaussianMixtureRarityCalculator


def _weighted_quantile(values: Sequence[float], weights: Sequence[float], quantile: float) -> float:
    """Compute the weighted quantile of `values` with corresponding `weights`."""
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    sorter = np.argsort(v)
    v_sorted = v[sorter]
    w_sorted = w[sorter]
    cumw = np.cumsum(w_sorted) - 0.5 * w_sorted
    cumw /= cumw[-1]
    return float(np.interp(quantile, cumw, v_sorted))


class BaseTypeRarityAggregator:
    """
    Aggregates listing counts per base type and computes percentile-based rarity tiers
    based on the distribution of individual-item rarity tiers.
    """
    def __init__(self, lower_quantile: float = 0.5, upper_quantile: float = 0.9) -> None:
        self._lower_quantile = lower_quantile
        self._upper_quantile = upper_quantile
        self._calculator = GaussianMixtureRarityCalculator()

    def aggregate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute total counts and percentile-based rarity tier for each base type.

        Args:
            df: DataFrame with columns ['Base Type', 'Rarity', 'Count']

        Returns:
            DataFrame with columns ['Base Type', 'total_count', 'rarity_tier']
        """
        df_copy = df.copy()
        records = []
        for base_type, group in df_copy.groupby('Base Type'):
            rarities = group['Rarity'].to_numpy(dtype=float)
            counts = group['Count'].to_numpy(dtype=float)
            total_count = int(counts.sum())

            # compute the weighted high-percentile tier (e.g., 90th percentile)
            tier = _weighted_quantile(rarities, counts, self._upper_quantile)
            # round up to nearest integer tier
            rarity_tier = int(np.ceil(tier))

            records.append({
                'Base Type': base_type,
                'total_count': total_count,
                'rarity_tier': rarity_tier
            })

        result_df = pd.DataFrame.from_records(records)
        return result_df
