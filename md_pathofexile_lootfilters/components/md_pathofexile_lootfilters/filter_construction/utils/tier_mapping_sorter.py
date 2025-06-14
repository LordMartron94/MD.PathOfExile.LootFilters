from typing import Dict, List, Tuple, Union, TypeVar, Callable, Generic, Sequence, Mapping

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier, parse_tier_value

T = TypeVar("T")
TierKey = Union[ItemTier, str]
TierParser = Callable[[str], ItemTier]


class TierKeyNormalizer(Generic[T]):
    """Normalize mapping keys to ItemTier using a TierParser."""

    def __init__(self, parser: TierParser = parse_tier_value) -> None:
        self._parser = parser

    def normalize(
            self,
            mapping: Mapping[TierKey, T]
    ) -> Dict[ItemTier, List[T]]:
        normalized: Dict[ItemTier, T] = {}
        for raw_key, values in mapping.items():
            if isinstance(raw_key, ItemTier):
                tier = raw_key
            elif isinstance(raw_key, str):
                tier = self._parser(raw_key)
            else:
                raise TypeError(
                    f"Mapping key must be ItemTier or str, got {type(raw_key)}"
                )
            normalized[tier] = values
        return normalized


class TierMappingSorter(Generic[T]):
    """Sorts a mapping from ItemTier to List[T], in the enum’s defined order."""

    def __init__(
            self,
            tiers: Sequence[ItemTier] = tuple(ItemTier),
            parser: TierParser = parse_tier_value,
    ) -> None:
        self._tiers = tiers
        self._normalizer = TierKeyNormalizer(parser)

    def sort(
            self,
            mapping: Mapping[TierKey, T]
    ) -> List[Tuple[ItemTier, T]]:
        normalized = self._normalizer.normalize(mapping)
        return [
            (tier, normalized[tier])
            for tier in self._tiers
            if tier in normalized
        ]
