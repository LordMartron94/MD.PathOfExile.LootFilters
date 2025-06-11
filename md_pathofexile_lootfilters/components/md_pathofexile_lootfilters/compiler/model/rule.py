from typing import List, Optional

import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class Rule(pydantic.BaseModel):
    rule_type: RuleType
    conditions: List[Condition] = []
    style: Optional[Style] = None
