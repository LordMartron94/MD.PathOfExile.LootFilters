import pprint
from typing import Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter

_SORTER = TierMappingSorter()

def log_tiers(logger: HoornLogger, tiers: Dict[str, int], log_separator: str, tiering_category: str):
    sorted_tiers = [{
        tier.value: count
    }
    for tier, count in _SORTER.sort(tiers)]
    logger.info(f"Tiers ({tiering_category}):\n{pprint.pformat(sorted_tiers)}", separator=log_separator)
