import pprint
from collections import defaultdict
from typing import List, Dict, Tuple

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import DATA_DIR
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.helpers.aggregation_rarity import \
    BaseTypeRarityAggregator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    sanitize_data_columns, BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier_rule_unique, get_tier_unique
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class HighlightUniques(IPipe):
    def __init__(
            self,
            logger: HoornLogger,
            condition_factory: ConditionFactory,
            rule_factory: RuleFactory,
            pipeline_prefix: str,
            section_heading: str
    ):
        self._logger = logger
        self._separator = f"{pipeline_prefix}.{self.__class__.__name__}"

        self._condition_factory = condition_factory
        self._rule_factory = rule_factory
        self._tier_mapping_sorter = TierMappingSorter()

        self._section_heading = section_heading
        self._section_description = (
            "Highlights every unique."
        )

    # noinspection PyUnresolvedReferences
    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        df = sanitize_data_columns(data.uniques_data)

        agg = BaseTypeRarityAggregator.aggregate(df)
        agg.to_csv(DATA_DIR / "uniques_intermediary_stats.csv", index=False)

        rules = []
        tier_counts: Dict[str,int] = defaultdict(int)

        mapping: Dict[ItemTier, List[Tuple]] = defaultdict(list)

        for row in agg.itertuples(index=False):
            tier = get_tier_unique(row, "rarity_median")
            mapping[tier].append(row)

        sorted_mapping: List[Tuple[ItemTier, List[Tuple]]] = self._tier_mapping_sorter.sort(mapping)

        for tier, rows in sorted_mapping:
            base_types: List[str] = [row.base_type for row in rows]
            rules.append(
                get_tier_rule_unique(
                    self._rule_factory,
                    self._condition_factory,
                    base_types,
                    tier,
                    tier_counts,
                    data,
                    BaseTypeCategory.uniques
                )
            )

        self._register_section(data, rules)

        self._logger.info(f"Tiers:\n{pprint.pformat(tier_counts)}", separator=self._separator)

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
