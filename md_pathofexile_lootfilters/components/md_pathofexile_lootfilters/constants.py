from pathlib import Path
from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import BuildType, \
    get_associated_equipments, EquipmentType, get_unassociated_equipments

APP_NAME: str = "MD.PathOfExile.LootFilters"
MAX_SEPARATOR_LENGTH: int = 50

DEBUG_MODE: bool = False
VERBOSE: bool = False

OUTPUT_DIRECTORIES: List[Path] = [
    Path(r"X:\MD.PathOfExile.LootFilters\output"),
    Path(r"C:\Users\LordMartron\Documents\My Games\Path of Exile")
]

SELECTED_BUILD_TYPE: BuildType = BuildType.MeleeSpellcaster

ASSOCIATED_EQUIPMENT: List[EquipmentType] = get_associated_equipments(SELECTED_BUILD_TYPE)
UNASSOCIATED_EQUIPMENT: List[EquipmentType] = get_unassociated_equipments(SELECTED_BUILD_TYPE)
