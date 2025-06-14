from abc import abstractmethod
from typing import Protocol, Dict, List, Tuple, Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier


class TierMapConstructor(Protocol):
    @abstractmethod
    def construct(
            self,
            dataframe: pd.DataFrame,
            mapping: Dict[ItemTier, List[Tuple]],
            accessors: Optional[Dict[str, str]] = None,
    ) -> None:
        ...
