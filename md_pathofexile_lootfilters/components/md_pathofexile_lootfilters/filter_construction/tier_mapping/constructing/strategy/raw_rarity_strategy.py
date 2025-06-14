from typing import Dict, List, Tuple, Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier_unique


class RawRarityMappingStrategy:
    """Constructs mapping based on single rarity column."""

    def construct(
            self,
            dataframe: pd.DataFrame,
            mapping: Dict[ItemTier, List[Tuple]],
            accessors: Optional[Dict[str, str]] = None,
    ) -> None:
        accessors = accessors or {}
        rarity_acc = accessors.get("rarity_accessor", "rarity_median")
        for row in dataframe.itertuples(index=False):
            tier = get_tier_unique(row, rarity_acc)
            mapping[tier].append(row)
