from collections import defaultdict
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.appending.strategy.single_tier_base_types import \
    SingleTierBaseTypesAppendingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.constructing.strategy.raw_rarity_and_usefulness_strategy import \
    RawRarityAndUsefulnessMappingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.tier_rule_applier import \
    TierRuleApplier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    filter_rows_by_category, BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.print_tiers import \
    log_tiers
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class AddMiscCurrenciesTiering(IPipe):
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
        self._tier_rule_applier = TierRuleApplier(logger, rule_factory, condition_factory, tier_mapping_sorter)

        self._section_heading = section_heading
        self._section_description = (
            "Tiers the miscellaneous currencies based on rarity and value."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        rules = self._get_rules(data)

        self._register_section(data, rules)

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data

    def _get_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        rules = []

        misc_currencies = filter_rows_by_category(BaseTypeCategory.misc, data.base_type_data)
        supplies = filter_rows_by_category(BaseTypeCategory.supplies, data.base_type_data)

        mapping = {
            BaseTypeCategory.misc: misc_currencies,
            BaseTypeCategory.supplies: supplies,
        }

        tier_counts: Dict[str, int] = defaultdict(int)

        for item_base_type_category, rows in mapping.items():
            self._tier_rule_applier.apply(
                rows,
                data,
                item_base_type_category,
                tier_counts,
                rules,
                mapping_strategy=RawRarityAndUsefulnessMappingStrategy(self._logger),
                appender_strategy=SingleTierBaseTypesAppendingStrategy(self._rule_factory, self._condition_factory),
                base_type_accessor="basetype",
                accessors={
                    "rarity_accessor": "rarity__1_6",
                    "usefulness_accessor": "usefulness__1_6",
                }
            )

        log_tiers(self._logger, tier_counts, self._separator, "Misc. Currencies")

        return rules

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
