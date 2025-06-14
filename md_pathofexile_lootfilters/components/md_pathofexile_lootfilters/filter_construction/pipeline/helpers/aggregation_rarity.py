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
        df['weighted'] = df['Rarity'] * df['Count']

        # Group and compute all metrics
        agg = df.groupby('Base Type').agg(
            total_count=('Count', 'sum'),
            rarity_avg=('weighted', lambda x: x.sum() / df.loc[x.index, 'Count'].sum()),
            rarity_median=('Rarity', 'median'),
            rarity_max=('Rarity', 'max'),
            rarity_std=('Rarity', 'std')
        ).reset_index()

        return agg
