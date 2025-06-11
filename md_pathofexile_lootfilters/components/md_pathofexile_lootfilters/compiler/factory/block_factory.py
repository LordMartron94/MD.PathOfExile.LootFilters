from typing import List, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class BlockFactory:
    """
    Factory for building loot filter blocks to be used downstream.
    """

    def __init__(self, logger: HoornLogger):
        self._logger: HoornLogger = logger
        self._separator: str = self.__class__.__name__
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def get_rule(self,
                 block_type: BlockType,
                 conditions: List[Condition],
                 style: Optional[Style]) -> Rule:
        self._logger.trace(f"Getting catch all block with type: \"{block_type.value}\"", separator=self._separator)
        return Rule(
            block_type=block_type,
            conditions=conditions,
            style=style
        )

    def get_catch_all_block(self, block_type: BlockType) -> Rule:
        self._logger.trace(f"Getting catch all block with type: \"{block_type.value}\"", separator=self._separator)
        return Rule(
            block_type=block_type,
            conditions=[]
        )
