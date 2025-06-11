from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import (
    Condition, ConditionKeyWord, ConditionOperator
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import (
    Act
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import UNASSOCIATED_EQUIPMENT
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.factory.show_hide_rule_builder import \
    ShowHideRuleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class AddClassWeaponsRules(IPipe):
    """
    Adds rules to hide all class-unrelated weapons except those found in Act 1,
    leveraging shared utility builders for maintainability.
    """

    def __init__(
            self,
            logger: HoornLogger,
            pipeline_prefix: str,
            section_heading: str
    ):
        self._logger = logger
        self._separator = f"{pipeline_prefix}.{self.__class__.__name__}"
        self._section_heading = section_heading
        self._section_description = (
            "Hides all class-unrelated weaponry -- except for those found in act 1."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        # 1) Determine style
        style: Style = data.style_preset_registry.get_style(
            ItemGroup.Equipment,
            ItemTier.NoTier
        )

        # 2) Build class-based condition group
        values = [item.value for item in UNASSOCIATED_EQUIPMENT]
        class_conditions: List[Condition] = ConditionGroupFactory.from_exact_values(
            data.condition_factory,
            keyword=ConditionKeyWord.Class,
            values=values,
            operator=ConditionOperator.exact_match,
            extra_conditions=ConditionGroupFactory.for_act_area_levels(
                data.condition_factory,
                Act.Act1
            )
        )

        # 3) Build show/hide rules
        show_rule, hide_rule = ShowHideRuleBuilder.build(
            rule_factory=data.rule_factory,
            show_conditions=class_conditions,
            hide_conditions=[class_conditions[0]],
            show_style=style
        )

        # 4) Register the new section
        data.generated_rules.append(
            RuleSection(
                heading=self._section_heading,
                description=self._section_description,
                rules=[show_rule, hide_rule]
            )
        )

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data
