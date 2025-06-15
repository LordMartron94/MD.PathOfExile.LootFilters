from typing import List, Optional

import numpy as np
from sklearn.mixture import GaussianMixture

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem


class GaussianMixtureRarityCalculator:
    """
    Assigns rarity tiers (1–n_tiers) by fitting a 1D Gaussian Mixture Model
    to log-transformed listing counts and ordering components by mean.
    Lower counts map to higher rarity tiers.
    """
    def __init__(
            self,
            n_tiers: int = 12,
            random_state: int = 42,
            covariance_type: str = 'full'
    ) -> None:
        self._n_tiers = n_tiers
        self._random_state = random_state
        self._covariance_type = covariance_type
        self._gmm: Optional[GaussianMixture] = None

    def calculate(self, items: List[GameItem]) -> None:
        """Calculate rarity tiers in-place for GameItem instances."""
        if not items:
            return
        counts = self._extract_counts(items)
        tiers = self._calculate_raw_tiers(counts)
        self._assign_tiers(items, tiers)

    def calculate_raw(self, counts: List[float]) -> List[int]:
        """Calculate rarity tiers from raw counts list."""
        if not counts:
            return []
        return self._calculate_raw_tiers(counts)

    @staticmethod
    def _extract_counts(items: List[GameItem]) -> List[float]:
        """Extract listing counts from GameItem objects."""
        return [float(item.listing_count) for item in items]

    @staticmethod
    def _log_transform(counts: np.ndarray) -> np.ndarray:
        """Apply log1p transform to counts."""
        return np.log1p(counts)

    def _initialize_model(self) -> GaussianMixture:
        """Instantiate the GaussianMixture model."""
        return GaussianMixture(
            n_components=self._n_tiers,
            covariance_type=self._covariance_type,
            random_state=self._random_state
        )

    def _fit_predict(self, log_counts: np.ndarray) -> np.ndarray:
        """Fit the GMM and predict component labels."""
        self._gmm = self._initialize_model()
        return self._gmm.fit_predict(log_counts)

    def _rank_components(self) -> dict:
        """
        Order components by their means and map to rarity tiers.
        Components with smaller means (rarer counts) get higher tier numbers.
        """
        if self._gmm is None:
            raise RuntimeError("Model has not been fitted yet.")
        means = self._gmm.means_.flatten()
        sorted_idx = np.argsort(means)
        return {comp: (self._n_tiers - rank) for rank, comp in enumerate(sorted_idx)}

    def _calculate_raw_tiers(self, counts: List[float]) -> List[int]:
        """Core pipeline: log-transform counts, fit GMM, and map labels to tiers."""
        arr = np.array(counts, dtype=float).reshape(-1, 1)
        log_counts = self._log_transform(arr)
        labels = self._fit_predict(log_counts)
        label_to_rank = self._rank_components()
        return [label_to_rank[int(lbl)] for lbl in labels]

    @staticmethod
    def _assign_tiers(items: List[GameItem], tiers: List[int]) -> None:
        """Assign computed tiers back to GameItem objects."""
        for item, tier in zip(items, tiers):
            item.rarity = tier
