from typing import List, Tuple

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition, ConditionKeyWord, ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import UNASSOCIATED_EQUIPMENT
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.factory.show_hide_rule_builder import ShowHideRuleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class ExcludeNonAssociatedWeaponry:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory

    def get_exclusion_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        """
        Orchestrates generation of exclusion rules: per-rarity show rules and a global hide rule.
        """
        styles = self._get_rarity_styles(data)
        class_conditions = self._get_base_class_conditions()
        act1_conditions = self._get_act1_conditions()

        show_rules = self._create_show_rules(styles, class_conditions, act1_conditions)
        hide_rule = self._create_hide_rule(class_conditions, act1_conditions)

        return show_rules + [hide_rule]

    @staticmethod
    def _get_rarity_styles(data: FilterConstructionPipelineContext) -> List[Tuple[str, Style]]:
        """
        Retrieves style presets for each rarity of EarlyWeaponry.
        """
        return [
            ("Normal", data.style_preset_registry.get_style(ItemGroup.EarlyWeaponry, ItemTier.LowTier3)),
            ("Magic", data.style_preset_registry.get_style(ItemGroup.EarlyWeaponry, ItemTier.LowTier2)),
            ("Rare", data.style_preset_registry.get_style(ItemGroup.EarlyWeaponry, ItemTier.LowTier1)),
        ]

    def _get_base_class_conditions(self) -> List[Condition]:
        """
        Builds conditions matching all Unassociated Equipment classes.
        """
        values = [item.value for item in UNASSOCIATED_EQUIPMENT]
        return ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            keyword=ConditionKeyWord.Class,
            values=values,
            operator=ConditionOperator.exact_match
        )

    def _get_act1_conditions(self) -> List[Condition]:
        """
        Builds conditions for Act I area levels.
        """
        return ConditionGroupFactory.for_act_area_levels(
            self._condition_factory,
            Act.Act1
        )

    def _create_show_rules(
            self,
            styles: List[Tuple[str, Style]],
            class_conditions: List[Condition],
            act1_conditions: List[Condition]
    ) -> List[Rule]:
        """
        Creates show rules for each rarity in Act I.
        """
        rules: List[Rule] = []
        for rarity, style in styles:
            rarity_conditions = ConditionGroupFactory.from_exact_values(
                self._condition_factory,
                keyword=ConditionKeyWord.Rarity,
                values=[rarity]
            )
            conditions = class_conditions + act1_conditions + rarity_conditions
            show_rule, _ = ShowHideRuleBuilder.build(
                rule_factory=self._rule_factory,
                show_conditions=conditions,
                hide_conditions=[],
                show_style=style
            )
            rules.append(show_rule)
        return rules

    def _create_hide_rule(
            self,
            class_conditions: List[Condition],
            act1_conditions: List[Condition]
    ) -> Rule:
        """
        Creates a hide rule for Normal and Magic rarities in Act I.
        """
        hide_rarities = ["Normal", "Magic", "Rare"]
        hide_conditions = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            keyword=ConditionKeyWord.Rarity,
            values=hide_rarities
        )
        _, hide_rule = ShowHideRuleBuilder.build(
            rule_factory=self._rule_factory,
            show_conditions=class_conditions + act1_conditions,
            hide_conditions=class_conditions + hide_conditions,
            show_style=None
        )
        return hide_rule
