from typing import Dict, Tuple, List, Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier, parse_tier_value


class GameRarityDesignationMappingStrategy:
    """Constructs mapping for normal, magic, and rare rarity tiers."""

    def construct(
            self,
            dataframe: pd.DataFrame,
            mapping: Dict[ItemTier, List[Tuple]],
            accessors: Optional[Dict[str, str]] = None,
    ) -> None:
        accessors = accessors or {}
        required = ["normal_accessor", "magic_accessor", "rare_accessor"]
        if not all(accessors.get(key) for key in required):
            raise ValueError("One of the rarity accessors is not defined.")

        for row in dataframe.itertuples(index=False):
            for key, label in [
                ("normal_accessor", "Normal"),
                ("magic_accessor", "Magic"),
                ("rare_accessor", "Rare"),
            ]:
                tier_value = getattr(row, accessors[key])
                tier = parse_tier_value(tier_value)
                mapping[tier].append((row, label))
