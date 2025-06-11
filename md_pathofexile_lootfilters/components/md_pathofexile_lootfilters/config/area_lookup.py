# ============ AREA LEVEL MAPPING ============
import enum
from typing import Dict, Tuple


class Act(enum.Enum):
    Act1 = "Act1"
    Act2 = "Act2"
    Act3 = "Act3"
    Act4 = "Act4"
    Act5 = "Act5"
    Act6 = "Act6"
    Act7 = "Act7"
    Act8 = "Act8"
    Act9 = "Act9"
    Act10 = "Act10"

# Internal mapping of each Act to its maximum level
_ACT_MAX_LEVEL_LOOKUP: Dict[Act, int] = {
    Act.Act1: 13,
    Act.Act2: 23,
    Act.Act3: 33,
    Act.Act4: 40,
    Act.Act5: 45,
    Act.Act6: 50,
    Act.Act7: 55,
    Act.Act8: 60,
    Act.Act9: 67,
    Act.Act10: 69,
}

# Public mapping of each Act to its (min_level, max_level) tuple
AREA_LEVEL_LOOKUP: Dict[Act, Tuple[int, int]] = {}
_prev_max: int = -1
for act in Act:
    max_level = _ACT_MAX_LEVEL_LOOKUP[act]
    min_level = 0 if _prev_max < 0 else _prev_max
    AREA_LEVEL_LOOKUP[act] = (min_level, max_level)
    _prev_max = max_level
