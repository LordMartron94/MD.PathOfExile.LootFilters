from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import AREA_LEVEL_LOOKUP, Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import UNASSOCIATED_EQUIPMENT
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class AddClassWeaponsRules(IPipe):
    def __init__(self, logger: HoornLogger, pipeline_prefix: str, section_heading: str):
        self._logger = logger
        self._separator: str = pipeline_prefix + "." + self.__class__.__name__

        self._section_heading = section_heading
        self._section_description: str = "Hides all class-unrelated weaponry -- except for those found in act 1."

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        rules: List[Rule] = []
        style: Style = data.style_preset_registry.get_style(ItemGroup.Equipment, ItemTier.NoTier)

        class_values: List[str] = []
        for unassociated_base in UNASSOCIATED_EQUIPMENT:
            class_values.append(unassociated_base.value)

        class_value_string: str = ""
        for class_value in class_values:
            class_value_string += f"\"{class_value}\" "

        class_condition = data.condition_factory.create_condition(ConditionKeyWord.Class, operator=ConditionOperator.exact_match, value=class_value_string)
        area_level_conditions = data.condition_factory.create_complex_area_level_condition(min_area_level=0, max_area_level=AREA_LEVEL_LOOKUP[Act.Act1])

        combined_conditions = [class_condition] + area_level_conditions

        show_rule = data.rule_factory.get_rule(BlockType.SHOW, conditions=combined_conditions, style=style)
        hide_rule = data.rule_factory.get_rule(BlockType.HIDE, conditions=[class_condition], style=None)

        rules.extend([show_rule, hide_rule])

        rule_section: RuleSection = RuleSection(
            heading=self._section_heading,
            description=self._section_description,
            rules=rules
        )

        data.generated_rules.append(rule_section)

        self._logger.info(f"Successfully added {self._section_heading} section!", separator=self._separator)

        return data
