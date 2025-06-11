from typing import List

import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import Condition


class Block(pydantic.BaseModel):
    block_type: BlockType
    conditions: List[Condition] = []
