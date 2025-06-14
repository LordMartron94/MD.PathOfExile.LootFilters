from collections import defaultdict
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    filter_rows_by_category, BaseTypeCategory, sanitize_data_columns
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.print_tiers import \
    log_tiers
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier_stack_based_rules


class AddLeagueSpecificDrops(IPipe):
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

        self._section_heading = section_heading
        self._section_description = (
            "Handles league specific mechanics."
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

        rows = filter_rows_by_category(BaseTypeCategory.gold, data.base_type_data)
        cleaned = sanitize_data_columns(rows)

        self._logger.debug(f"Cleaned: \n{cleaned.to_string()}", separator=self._separator)

        tier_counts: Dict[str, int] = defaultdict(int)

        for row in cleaned.itertuples(index=False):
            rules.extend(get_tier_stack_based_rules(self._rule_factory, self._condition_factory, row, tier_counts, data, BaseTypeCategory.gold, stack_mapping={
                500: ItemTier.HighTier3,
                200: ItemTier.MidTier1,
                50: ItemTier.MidTier2,
                1: ItemTier.MidTier3,
            }))

        log_tiers(self._logger, tier_counts, self._separator, "League Specific")

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
