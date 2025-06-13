from typing import Dict, Tuple

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
    ItemTier, get_tier_from_rarity_and_use
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


def _get_tier_currency_rule(rule_factory: RuleFactory, condition_factory: ConditionFactory, style: Style, base: str, tier: ItemTier) -> Rule:
    type_condition = condition_factory.create_condition(ConditionKeyWord.BaseType, operator=ConditionOperator.exact_match, value=f'"{base}"')
    area_conditions = ConditionGroupFactory.between_acts(condition_factory, Act.Act1, Act.Act10)

    rule = rule_factory.get_rule(
        rule_type=RuleType.SHOW,
        conditions=[type_condition] + area_conditions,
        style=style,
    )

    rule.comment = f"Tier: \"{tier.value}\""

    return rule


# noinspection PyUnresolvedReferences
def get_tier_currency_rule(
        rule_factory: RuleFactory,
        condition_factory: ConditionFactory,
        row: Tuple,
        tier_counts: Dict[str, int],
        data: FilterConstructionPipelineContext,
        type_category: BaseTypeCategory):
    rarity = getattr(row, "rarity__1_6")
    usefulness = getattr(row, "usefulness__1_6")

    tier = get_tier_from_rarity_and_use(rarity, usefulness)
    tier_counts[tier.value] += 1
    style      = determine_style(data, tier, type_category)
    return _get_tier_currency_rule(rule_factory, condition_factory, style, row.basetype, tier)
