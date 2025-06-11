from pathlib import Path
from typing import List

APP_NAME: str = "MD.PathOfExile.LootFilters"
MAX_SEPARATOR_LENGTH: int = 50

DEBUG_MODE: bool = True
VERBOSE: bool = False

OUTPUT_DIRECTORIES: List[Path] = [
    Path(r"X:\MD.PathOfExile.LootFilters\output"),
    Path(r"C:\Users\LordMartron\Documents\My Games\Path of Exile")
]
