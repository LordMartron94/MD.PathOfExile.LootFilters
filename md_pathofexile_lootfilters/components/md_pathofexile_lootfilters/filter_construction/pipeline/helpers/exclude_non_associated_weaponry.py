from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition, \
    ConditionKeyWord, ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import UNASSOCIATED_EQUIPMENT
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.factory.show_hide_rule_builder import \
    ShowHideRuleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class ExcludeNonAssociatedWeaponry:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory

    def get_exclusion_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        style = self._determine_style(data)
        class_conditions = self._build_class_conditions()
        show, hide = self._build_show_hide_rules(class_conditions, style)
        return [show, hide]

    @staticmethod
    def _determine_style(data: FilterConstructionPipelineContext) -> Style:
        return data.style_preset_registry.get_style(
            ItemGroup.EarlyWeaponry,
            ItemTier.LowTier1
        )

    def _build_class_conditions(
            self
    ) -> List[Condition]:
        values = [item.value for item in UNASSOCIATED_EQUIPMENT]

        rarity_conditions = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            keyword=ConditionKeyWord.Rarity,
            values=["Normal", "Magic", "Rare"]
        )

        base_conditions = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            keyword=ConditionKeyWord.Class,
            values=values,
            operator=ConditionOperator.exact_match,
            extra_conditions=rarity_conditions + ConditionGroupFactory.for_act_area_levels(
                self._condition_factory,
                Act.Act1
            )
        )
        return base_conditions

    def _build_show_hide_rules(
            self,
            class_conditions: List[Condition],
            style: Style
    ):
        return ShowHideRuleBuilder.build(
            rule_factory=self._rule_factory,
            show_conditions=class_conditions,
            hide_conditions=class_conditions[0:2],
            show_style=style
        )
