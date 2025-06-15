from typing import List, Tuple, Dict

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.game_item_extraction.model.game_item import \
    GameItem


class DuplicateAggregator:
    """
    Aggregates exact-duplicate GameItem instances (same Base Type & Item Name)
    by summing their listing_count and count.
    """
    @staticmethod
    def aggregate(items: List[GameItem]) -> List[GameItem]:
        grouped: Dict[Tuple[str, str], GameItem] = {}
        for item in items:
            key = (item.base_type, item.name)
            if key not in grouped:
                # create a shallow copy to avoid mutating original
                grouped[key] = GameItem(
                    name=item.name,
                    base_type=item.base_type,
                    listing_count=item.listing_count,
                    count=item.count
                )
            else:
                agg = grouped[key]
                agg.listing_count += item.listing_count
                agg.count += item.count
        return list(grouped.values())
