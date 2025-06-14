from collections import defaultdict
from typing import Dict, List, Optional

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.appending.appender import \
    Appender
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.appending.strategy.single_tier_base_types import \
    SingleTierBaseTypesAppendingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.constructing.strategy.raw_rarity_and_usefulness_strategy import \
    RawRarityAndUsefulnessMappingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.constructing.tier_map_constructor import \
    TierMapConstructor
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory, sanitize_data_columns
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class TierRuleApplier:
    """Orchestrates mapping and appending of tier rules."""

    def __init__(
            self,
            rule_factory: RuleFactory,
            condition_factory: ConditionFactory,
            tier_mapping_sorter: TierMappingSorter,
    ):
        self._rule_factory = rule_factory
        self._condition_factory = condition_factory
        self._sorter = tier_mapping_sorter

    def apply(
            self,
            dataframe: pd.DataFrame,
            data: FilterConstructionPipelineContext,
            base_type_category: BaseTypeCategory,
            tier_counts: Dict[str, int],
            rules: List[Rule],
            base_type_accessor: Optional[str] = None,
            mapping_strategy: TierMapConstructor = RawRarityAndUsefulnessMappingStrategy(),
            appender_strategy: Appender | None = None,
            accessors: Optional[Dict[str, str]] = None,
    ) -> None:
        appender_strategy = appender_strategy or SingleTierBaseTypesAppendingStrategy(
            rule_factory=self._rule_factory,
            condition_factory=self._condition_factory,
        )

        sanitized = sanitize_data_columns(dataframe)
        mapping: Dict[ItemTier, List] = defaultdict(list)
        mapping_strategy.construct(sanitized, mapping, accessors)

        for tier, rows_data in self._sorter.sort(mapping):
            new_rules = appender_strategy.append(
                rows_data,
                tier,
                tier_counts,
                data,
                base_type_accessor,
                base_type_category
            )
            rules.extend(new_rules)
