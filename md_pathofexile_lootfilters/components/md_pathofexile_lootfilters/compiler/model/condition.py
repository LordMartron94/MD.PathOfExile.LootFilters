import enum
from typing import Any, Optional

import pydantic

class ConditionKeyWord(enum.Enum):
    BaseEvasion = "BaseEvasion"
    AreaLevel = "AreaLevel"
    Rarity = "Rarity"
    BaseType = "BaseType"
    ItemLevel = "ItemLevel"
    Class = "Class"
    StackSize = "StackSize"

class ConditionOperator(enum.Enum):
    equal = "="
    not_equal = "!"
    not_equal2 = "!="
    less_than_or_equal = "<="
    greater_than_or_equal = ">="
    less_than = "<"
    greater_than = ">"
    exact_match = "=="

class Condition(pydantic.BaseModel):
    keyword: ConditionKeyWord
    operator: Optional[ConditionOperator] = None
    value: Any
