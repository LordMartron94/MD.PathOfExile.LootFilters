from collections import defaultdict
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import DATA_DIR
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.helpers.aggregation_rarity import \
    BaseTypeRarityAggregator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.appending.strategy.single_tier_base_types import \
    SingleTierBaseTypesAppendingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.constructing.strategy.raw_rarity_strategy import \
    RawRarityMappingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.tier_rule_applier import \
    TierRuleApplier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.print_tiers import \
    log_tiers
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class HighlightUniques(IPipe):
    def __init__(
            self,
            logger: HoornLogger,
            condition_factory: ConditionFactory,
            rule_factory: RuleFactory,
            tier_mapping_sorter: TierMappingSorter,
            pipeline_prefix: str,
            section_heading: str
    ):
        self._logger = logger
        self._separator = f"{pipeline_prefix}.{self.__class__.__name__}"

        self._condition_factory = condition_factory
        self._rule_factory = rule_factory
        self._tier_mapping_sorter = tier_mapping_sorter
        self._tier_rule_applier = TierRuleApplier(rule_factory, condition_factory, tier_mapping_sorter)

        self._aggregator = BaseTypeRarityAggregator()

        self._section_heading = section_heading
        self._section_description = (
            "Highlights every unique."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        agg = self._aggregator.aggregate(data.uniques_data)
        agg.to_csv(DATA_DIR / "uniques_intermediary_stats.csv", index=False)

        rules = []
        tier_counts: Dict[str,int] = defaultdict(int)

        self._tier_rule_applier.apply(
            agg,
            data,
            BaseTypeCategory.uniques,
            tier_counts,
            rules,
            mapping_strategy=RawRarityMappingStrategy(),
            appender_strategy=SingleTierBaseTypesAppendingStrategy(self._rule_factory, self._condition_factory),
            base_type_accessor="base_type",
            accessors={
                "rarity_accessor": "rarity_score"
            }
        )

        self._register_section(data, rules)

        log_tiers(self._logger, tier_counts, self._separator, "Uniques")

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data

    def _register_section(
            self,
            data: FilterConstructionPipelineContext,
            rules: List[Rule]
    ) -> None:
        data.generated_rules.append(
            RuleSection(
                heading=self._section_heading,
                description=self._section_description,
                rules=rules
            )
        )
