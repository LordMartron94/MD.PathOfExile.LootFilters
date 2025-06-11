import traceback
from pathlib import Path
from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.compiler import FilterCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import BlockFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import AREA_LEVEL_LOOKUP, Act
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
        blocks: List[Rule] = []
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

    def _get_hide_unassociated_equipment(self) -> List[Rule]:
        rules: List[Rule] = []
        style: Style = self._style_preset_registry.get_style(ItemGroup.Equipment, ItemTier.NoTier)

        class_values: List[str] = []
        for unassociated_base in UNASSOCIATED_EQUIPMENT:
            class_values.append(unassociated_base.value)

        class_value_string: str = ""
        for class_value in class_values:
            class_value_string += f"\"{class_value}\" "

        class_condition = self._condition_factory.create_condition(ConditionKeyWord.Class, operator=ConditionOperator.exact_match, value=class_value_string)
        area_level_conditions = self._condition_factory.create_complex_area_level_condition(min_area_level=0, max_area_level=AREA_LEVEL_LOOKUP[Act.Act1])

        combined_conditions = [class_condition] + area_level_conditions

        show_rule = self._block_factory.get_rule(BlockType.SHOW, conditions=combined_conditions, style=style)
        hide_rule = self._block_factory.get_rule(BlockType.HIDE, conditions=[class_condition], style=None)

        rules.extend([show_rule, hide_rule])

        return rules

    def _get_catchall(self) -> Rule:
        catch_all_block: Rule = self._block_factory.get_catch_all_block(BlockType.SHOW)
        catch_all_block.style = self._style_preset_registry.get_style(ItemGroup.CatchAll, ItemTier.NoTier)
        return catch_all_block
