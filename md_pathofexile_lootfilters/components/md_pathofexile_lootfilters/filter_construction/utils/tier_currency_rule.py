from typing import Dict, Tuple, List, Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier, get_tier_from_rarity_and_use, get_tier_from_rarity
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.quoted_value_list_builder import \
    QuotedValueListBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


def _get_base_rule(
        rule_factory: RuleFactory,
        condition_factory: ConditionFactory,
        style: Style,
        base: str | List[str],
        tier: ItemTier,
        extra_conditions: Optional[List[Condition]] = None
) -> Rule:
    if extra_conditions is None:
        extra_conditions = []

    base = base if isinstance(base, list) else [base]
    type_condition = condition_factory.create_condition(ConditionKeyWord.BaseType, operator=ConditionOperator.exact_match, value=QuotedValueListBuilder.build(base))
    area_conditions = ConditionGroupFactory.between_acts(condition_factory, Act.Act1, Act.Act10)

    rule = rule_factory.get_rule(
        rule_type=RuleType.SHOW,
        conditions=[type_condition] +extra_conditions + area_conditions,
        style=style,
    )

    rule.comment = f"Tier: \"{tier.value}\""

    return rule

# noinspection PyUnresolvedReferences
def get_tier_stack_based_rules(
        rule_factory: RuleFactory,
        condition_factory: ConditionFactory,
        row: Tuple,
        tier_counts: Dict[str, int],
        data: FilterConstructionPipelineContext,
        type_category: BaseTypeCategory,
        stack_mapping: Dict[int, ItemTier]
) -> List[Rule]:
    rules: List[Rule] = []

    for min_stack_size, tier in stack_mapping.items():
        tier_counts[tier.value] += 1
        style      = determine_style(data, tier, type_category)
        stack_condition = condition_factory.create_condition(ConditionKeyWord.StackSize, operator=ConditionOperator.greater_than_or_equal, value=min_stack_size)
        rules.append(_get_base_rule(rule_factory, condition_factory, style, row.basetype, tier, extra_conditions=[stack_condition]))

    return rules

def get_tier_unique(
        row: Tuple,
        rarity_accessor: str
) -> ItemTier:
    rarity = getattr(row, rarity_accessor)
    tier = get_tier_from_rarity(rarity)
    return tier

def get_tier(row: Tuple, rarity_accessor: str | None = None, usefulness_accessor: str | None = None) -> ItemTier:
    rarity = getattr(row, "rarity__1_6" if not rarity_accessor else rarity_accessor)
    usefulness = getattr(row, "usefulness__1_6" if not usefulness_accessor else usefulness_accessor)
    return get_tier_from_rarity_and_use(rarity, usefulness)

# noinspection PyUnresolvedReferences
def get_tier_rule(
        rule_factory: RuleFactory,
        condition_factory: ConditionFactory,
        base_types: List[str],
        tier: ItemTier,
        tier_counts: Dict[str, int],
        data: FilterConstructionPipelineContext,
        type_category: BaseTypeCategory,
) -> Rule:
    tier_counts[tier.value] += len(base_types)
    style      = determine_style(data, tier, type_category)
    return _get_base_rule(rule_factory, condition_factory, style, base_types, tier)
