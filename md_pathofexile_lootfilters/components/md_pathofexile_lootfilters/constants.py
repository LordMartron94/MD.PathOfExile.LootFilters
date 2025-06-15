from pathlib import Path
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import BuildType, \
    get_associated_weapons, WeaponTypeClass, get_unassociated_weapons

# ---- Configurable ----
APP_NAME: str = "MD.PathOfExile.LootFilters"
APP_VERSION: str = "1.0.0"
CONTACT: str = "md.career@protonmail.com"
MAX_SEPARATOR_LENGTH: int = 80

DEBUG_MODE: bool = False
VERBOSE: bool = False

BUILD_TEST_FILTER: bool = False

OUTPUT_DIRECTORIES: List[Path] = [
    Path(r"X:\MD.PathOfExile.LootFilters\output"),
    Path(r"C:\Users\LordMartron\Documents\My Games\Path of Exile")
]

PATH_OF_BUILDING_DATA_DIR: Path = Path(r"D:\[02] Modding\[01] Tools\[08] Path of Building\Path of Building Community\Data")

LEAGUE_WEIGHTS: Dict[str, float] = { # -- IMPORTANT for Economy Data retrieval
    "Hardcore": 1.00,
    "Hardcore Mercenaries": 0.75,
    "HC Settlers": 0.50,
    "Standard": 0.90,
    "Mercenaries": 0.60,
    "Settlers": 0.40,
}

# ---- Automatic ----
ROOT: Path = Path(__file__).parent.parent.parent.parent
CONFIG_DIR: Path =  ROOT / "md_pathofexile_lootfilters" / "components" / "md_pathofexile_lootfilters" / "config"
DATA_DIR: Path = ROOT / "data"

FILTER_NAME: str = "MD.TestFilter.filter" if BUILD_TEST_FILTER else "MD.SSF-SC&HC-Filter.filter"

SELECTED_BUILD_TYPE: BuildType = BuildType.MeleeSpellcaster

ASSOCIATED_WEAPONRY: List[WeaponTypeClass] = get_associated_weapons(SELECTED_BUILD_TYPE)
UNASSOCIATED_WEAPONRY: List[WeaponTypeClass] = get_unassociated_weapons(SELECTED_BUILD_TYPE)

USER_AGENT: str = f"{APP_NAME}/{APP_VERSION} - (contact: {CONTACT})"
