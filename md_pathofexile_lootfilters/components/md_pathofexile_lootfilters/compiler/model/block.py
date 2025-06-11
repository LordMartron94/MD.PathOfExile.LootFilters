import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType


class Block(pydantic.BaseModel):
    block_type: BlockType
