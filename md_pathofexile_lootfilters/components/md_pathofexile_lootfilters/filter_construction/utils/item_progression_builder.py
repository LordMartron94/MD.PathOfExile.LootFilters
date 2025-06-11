from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class ItemProgressionBuilder:
    @staticmethod
    def get_progression_rules(condition_factory: ConditionFactory,
                              rule_factory: RuleFactory,
                              item_progression: List[ItemProgressionItem],
                              normal_style: Style,
                              magic_style: Style,
                              rare_style: Style) -> List[Rule]:
        rules = []

        for item_progression_item in item_progression:
            normal_condition = condition_factory.create_condition(ConditionKeyWord.Rarity, operator=None, value="Normal")
            magic_condition = condition_factory.create_condition(ConditionKeyWord.Rarity, operator=None, value="Magic")
            rare_condition = condition_factory.create_condition(ConditionKeyWord.Rarity, operator=None, value="Rare")

            base_type_condition = condition_factory.create_condition(ConditionKeyWord.BaseType, operator=None, value=item_progression_item.base_type.value)
            start_level_condition = condition_factory.create_condition(ConditionKeyWord.ItemLevel, operator=ConditionOperator.greater_than_or_equal, value=item_progression_item.start_level)
            end_level_condition = condition_factory.create_condition(ConditionKeyWord.ItemLevel, operator=ConditionOperator.less_than_or_equal, value=item_progression_item.end_level)

            rules.append(rule_factory.get_rule(RuleType.SHOW, [base_type_condition, normal_condition, start_level_condition, end_level_condition], normal_style))
            rules.append(rule_factory.get_rule(RuleType.SHOW,  [base_type_condition, magic_condition, start_level_condition, end_level_condition], magic_style))
            rules.append(rule_factory.get_rule(RuleType.SHOW, [base_type_condition, rare_condition, start_level_condition, end_level_condition], rare_style))

        return rules
