# ============ AREA LEVEL MAPPING ============
import enum
from typing import Dict


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

AREA_LEVEL_LOOKUP: Dict[Act, int] = {
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
