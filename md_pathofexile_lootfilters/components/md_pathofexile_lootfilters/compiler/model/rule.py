from typing import List, Optional

import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class Rule(pydantic.BaseModel):
    block_type: BlockType
    conditions: List[Condition] = []
    style: Optional[Style] = None
