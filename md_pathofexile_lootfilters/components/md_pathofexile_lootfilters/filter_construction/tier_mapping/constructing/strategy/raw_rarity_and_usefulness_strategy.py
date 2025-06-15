from typing import Dict, List, Tuple, Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier


class RawRarityAndUsefulnessMappingStrategy:
    """Constructs mapping using rarity and usefulness columns."""
    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__

    def construct(
            self,
            dataframe: pd.DataFrame,
            mapping: Dict[ItemTier, List[Tuple]],
            accessors: Optional[Dict[str, str]] = None,
    ) -> None:
        accessors = accessors or {}
        rarity_acc = accessors.get("rarity_accessor")
        usefulness_acc = accessors.get("usefulness_accessor")
        basetype_acc = accessors.get("basetype_accessor")
        if not rarity_acc or not usefulness_acc or not basetype_acc:
            raise ValueError("Missing 'rarity_accessor' or 'usefulness_accessor' or 'basetype_accessor'.")
        for row in dataframe.itertuples(index=False):
            tier = get_tier(
                self._logger,
                self._separator,
                row,
                rarity_accessor=rarity_acc,
                usefulness_accessor=usefulness_acc,
                base_type_accessor=basetype_acc,
            )
            mapping[tier].append(row)
