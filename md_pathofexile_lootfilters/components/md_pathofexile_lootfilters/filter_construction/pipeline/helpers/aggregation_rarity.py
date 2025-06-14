import pandas as pd


class BaseTypeRarityAggregator:
    """Aggregate per-base-type rarity statistics from a uniques-level DataFrame."""
    @staticmethod
    def _weighted_avg(series: pd.Series, weights: pd.Series) -> float:
        return (series * weights).sum() / weights.sum()

    @classmethod
    def aggregate(cls, df: pd.DataFrame) -> pd.DataFrame:
        # Pre-compute the weighted component
        df = df.copy()
        df['weighted'] = df['rarity'] * df['count']

        # Group and compute all metrics
        agg = df.groupby('base_type').agg(
            total_count=('count', 'sum'),
            rarity_avg=('weighted', lambda x: x.sum() / df.loc[x.index, 'count'].sum()),
            rarity_median=('rarity', 'median'),
            rarity_max=('rarity', 'max'),
            rarity_std=('rarity', 'std')
        ).reset_index()

        return agg
