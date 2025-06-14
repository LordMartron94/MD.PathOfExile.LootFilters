from typing import Any, Dict, List, Tuple, Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier


class TierMappingSorter:
    """Sorts a mapping from ItemTier to lists, in enum definition order."""

    def __init__(self, tiers: Optional[List[ItemTier]] = None):
        self._tiers = tiers or list(ItemTier)

    def sort(
            self,
            mapping: Dict[ItemTier, List[Any]]
    ) -> List[Tuple[ItemTier, List[Any]]]:
        sorted_pairs: List[Tuple[ItemTier, List[Any]]] = []
        for tier in self._tiers:
            if tier in mapping:
                sorted_pairs.append((tier, mapping[tier]))
        return sorted_pairs
