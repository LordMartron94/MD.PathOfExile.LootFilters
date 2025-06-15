from typing import List, Tuple, Dict, Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier_rule


class SingleTierBaseTypesAppendingStrategy:
    """Appends a single tier rule based on base types."""

    def __init__(
            self,
            rule_factory: RuleFactory,
            condition_factory: ConditionFactory,
            extra_conditions: List[Condition] | None = None,
    ) -> None:
        self._rule_factory = rule_factory
        self._condition_factory = condition_factory
        self._extra_conditions = extra_conditions or []

    def append(
            self,
            rows_data: List[Tuple],
            tier: ItemTier,
            tier_counts: Dict[str, int],
            data: FilterConstructionPipelineContext,
            base_type_accessor: Optional[str],
            base_type_category: BaseTypeCategory,
    ) -> List[Rule]:
        base_types = [
            getattr(row, base_type_accessor or "base_type", "")
            for row in rows_data
        ]
        rule = get_tier_rule(
            self._rule_factory,
            self._condition_factory,
            base_types,
            tier,
            tier_counts,
            data,
            base_type_category,
            extra_conditions=self._extra_conditions
        )
        return [rule]
