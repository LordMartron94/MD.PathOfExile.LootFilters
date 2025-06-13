from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


def get_tier_currency_rule(rule_factory: RuleFactory, condition_factory: ConditionFactory, style: Style, base: str, tier: ItemTier) -> Rule:
    type_condition = condition_factory.create_condition(ConditionKeyWord.BaseType, operator=ConditionOperator.exact_match, value=f'"{base}"')
    area_conditions = ConditionGroupFactory.between_acts(condition_factory, Act.Act1, Act.Act10)

    rule = rule_factory.get_rule(
        rule_type=RuleType.SHOW,
        conditions=[type_condition] + area_conditions,
        style=style,
    )

    rule.comment = f"Tier: \"{tier.value}\""

    return rule
