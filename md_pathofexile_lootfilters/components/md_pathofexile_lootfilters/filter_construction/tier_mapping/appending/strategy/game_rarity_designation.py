from itertools import groupby
from typing import Tuple, List, Dict, Optional

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
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.quoted_value_list_builder import \
    QuotedValueListBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class GameRarityAppender:
    """
    Appends SHOW rules for items grouped by game rarity (Normal, Magic, Rare).
    """

    def __init__(
            self,
            rule_factory: RuleFactory,
            condition_factory: ConditionFactory,
            act_mappings: Dict[str, Tuple[Act, Act]]
    ) -> None:
        self._rule_factory = rule_factory
        self._condition_factory = condition_factory
        self._act_mappings = act_mappings

    def append(
            self,
            rows_data: List[Tuple[object, str]],
            tier: ItemTier,
            tier_counts: Dict[str, int],
            data: FilterConstructionPipelineContext,
            base_type_accessor: Optional[str],
            base_type_category: BaseTypeCategory,
    ) -> List[Rule]:
        style = determine_style(data, tier, base_type_category)
        sorted_data = sorted(rows_data, key=lambda pair: pair[1])
        rules: List[Rule] = []

        for rarity, group in groupby(sorted_data, key=lambda pair: pair[1]):
            rows, _ = zip(*list(group))
            bases = [getattr(row, base_type_accessor or "base_type", "") for row in rows]
            rules.append(self._build_rule(rarity, bases, tier, style, tier_counts))

        return rules

    def _build_rule(
            self,
            rarity: str,
            bases: List[str],
            tier: ItemTier,
            style: Style,
            tier_counts: Dict[str, int],
    ) -> Rule:
        type_cond = self._condition_factory.create_condition(
            ConditionKeyWord.BaseType,
            operator=ConditionOperator.exact_match,
            value=QuotedValueListBuilder.build(bases),
        )
        rarity_cond = self._condition_factory.create_condition(
            ConditionKeyWord.Rarity,
            operator=ConditionOperator.exact_match,
            value=f'"{rarity}"',
        )
        area_conds = self._area_conditions(rarity)

        rule = self._rule_factory.get_rule(
            rule_type=RuleType.SHOW,
            conditions=[type_cond, rarity_cond] + area_conds,
            style=style,
        )
        rule.comment = f"Tier: \"{tier.value}\""
        tier_counts[tier.value] += len(bases)
        return rule

    def _area_conditions(self, rarity: str) -> List:
        start_act, end_act = self._act_mappings.get(rarity, (None, None))

        if start_act is not None and end_act is not None:
            return ConditionGroupFactory.between_acts(self._condition_factory, start_act, end_act)

        return ConditionGroupFactory.between_acts(self._condition_factory, Act.Act1, Act.Act10)
