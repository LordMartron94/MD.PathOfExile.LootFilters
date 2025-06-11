import traceback
from pathlib import Path
from typing import Tuple, List, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.compiler import FilterCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import ConditionKeyWord
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import BlockFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.block import Block
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import OUTPUT_DIRECTORIES, \
    UNASSOCIATED_EQUIPMENT
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.style_preset_registry import \
    StylePresetRegistry
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class FilterConstructor:
    """
    High-Level API/Class to handle the construction of loot filters.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__

        self._block_factory: BlockFactory = BlockFactory(logger)
        self._condition_factory: ConditionFactory = ConditionFactory()
        self._compiler: FilterCompiler = FilterCompiler(logger)
        self._style_preset_registry: StylePresetRegistry = StylePresetRegistry(logger)

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def construct_filter(self) -> None:
        blocks: List[Tuple[Block, Optional[Style]]] = []
        blocks.extend(self._get_hide_unassociated_equipment())
        blocks.append(self._get_catchall())

        transformed_str: List[str] = self._compiler.transform_batch_blocks(blocks)

        for output_dir in OUTPUT_DIRECTORIES:
            filter_path: Path = output_dir / "MD.TestFilter.filter"

            try:
                with open(filter_path, "w") as filter_file:
                    filter_file.write('\n'.join(transformed_str))
            except Exception as e:
                tb = traceback.format_exc()
                self._logger.error(f"Something went wrong while outputting to \"{filter_path}\". Exception: \"{e}\"\n{tb}", separator=self._separator)

            self._logger.info(f"Output written to \"{filter_path}\".", separator=self._separator)

    def _get_hide_unassociated_equipment(self) -> List[Tuple[Block, Optional[Style]]]:
        rules: List[Tuple[Block, Optional[Style]]] = []

        for unassociated_base in UNASSOCIATED_EQUIPMENT:
            condition = self._condition_factory.create_condition(ConditionKeyWord.Class, operator=None, value=unassociated_base.value)
            rule = self._block_factory.get_rule(BlockType.HIDE, conditions=[condition])
            rules.append((rule, None))

        return rules

    def _get_catchall(self) -> Tuple[Block, Style]:
        catch_all_block: Block = self._block_factory.get_catch_all_block(BlockType.SHOW)
        style: Style = self._style_preset_registry.get_style(ItemGroup.CatchAll, ItemTier.NoTier)
        return catch_all_block, style
