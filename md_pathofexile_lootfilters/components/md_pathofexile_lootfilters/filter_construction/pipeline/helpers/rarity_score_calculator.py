from typing import Sequence

import numpy as np


class RarityScoreCalculator:
    def __init__(
            self,
            lower_quantile: float = 0.5,
            upper_quantile: float = 0.9,
            lower_weight: float = 0.8,
            upper_weight: float = 0.2,
    ) -> None:
        """
        Calculates a blended rarity score for groups of items based on weighted quantiles.

        Attributes:
            lower_quantile: float - the lower quantile to use (e.g., 0.5 for median).
            upper_quantile: float - the upper quantile to use (e.g., 0.9 for 90th percentile).
            lower_weight: float - weight for the lower_quantile score in blending.
            upper_weight: float - weight for the upper_quantile score in blending.
        """

        if not 0 <= lower_quantile < upper_quantile <= 1:
            raise ValueError("Quantiles must satisfy 0 <= lower < upper <= 1")
        if not np.isclose(lower_weight + upper_weight, 1.0):
            raise ValueError("Weights must sum to 1")
        self._lower_quantile = lower_quantile
        self._upper_quantile = upper_quantile
        self._lower_weight = lower_weight
        self._upper_weight = upper_weight

    @staticmethod
    def _weighted_quantile(
            values: Sequence[float],
            weights: Sequence[float],
            quantile: float
    ) -> float:
        """
        Compute the weighted quantile of `values` with corresponding `weights`.
        """
        v = np.asarray(values, dtype=float)
        w = np.asarray(weights, dtype=float)
        sorter = np.argsort(v)
        v_sorted = v[sorter]
        w_sorted = w[sorter]
        # center weights on values
        cumw = np.cumsum(w_sorted) - 0.5 * w_sorted
        cumw /= cumw[-1]
        return float(np.interp(quantile, cumw, v_sorted))

    def compute_score(
            self,
            rarities: Sequence[float],
            counts: Sequence[float]
    ) -> float:
        """
        Compute a blended rarity score for a group of items.

        Args:
            rarities: sequence of rarity values (e.g., 1-12 per unique)
            counts: sequence of counts (listing_count per unique)

        Returns:
            A single float rarity score.
        """
        r = np.asarray(rarities, dtype=float)
        c = np.asarray(counts, dtype=float)
        # Handle edge cases: no data or uniform rarity
        if r.size == 0 or c.sum() == 0 or np.all(r == r[0]):
            return float(r[0]) if r.size > 0 else 0.0

        low = self._weighted_quantile(r, c, self._lower_quantile)
        high = self._weighted_quantile(r, c, self._upper_quantile)

        return self._lower_weight * low + self._upper_weight * high
