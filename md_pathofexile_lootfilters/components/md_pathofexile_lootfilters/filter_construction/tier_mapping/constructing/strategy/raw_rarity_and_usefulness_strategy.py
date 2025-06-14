from typing import Dict, List, Tuple, Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier


class RawRarityAndUsefulnessMappingStrategy:
    """Constructs mapping using rarity and usefulness columns."""

    def construct(
            self,
            dataframe: pd.DataFrame,
            mapping: Dict[ItemTier, List[Tuple]],
            accessors: Optional[Dict[str, str]] = None,
    ) -> None:
        accessors = accessors or {}
        rarity_acc = accessors.get("rarity_accessor")
        usefulness_acc = accessors.get("usefulness_accessor")
        if not rarity_acc or not usefulness_acc:
            raise ValueError("Missing 'rarity_accessor' or 'usefulness_accessor'.")
        for row in dataframe.itertuples(index=False):
            tier = get_tier(
                row,
                rarity_accessor=rarity_acc,
                usefulness_accessor=usefulness_acc,
            )
            mapping[tier].append(row)
