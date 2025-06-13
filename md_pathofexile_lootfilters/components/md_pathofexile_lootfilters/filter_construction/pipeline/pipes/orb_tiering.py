import pprint
from collections import defaultdict
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    get_tier_from_rarity_and_use
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    filter_rows_by_category, BaseTypeCategory, sanitize_data_columns
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_orb_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_currency_rule import \
    get_tier_currency_rule


class AddOrbTiering(IPipe):
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
            "Tiers the orbs based on rarity and value."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        rules = self._get_rules(data)

        self._register_section(data, rules)

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data

    # noinspection PyUnresolvedReferences
    def _get_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        rules = []

        rows = filter_rows_by_category(BaseTypeCategory.orbs, data.base_type_data)
        cleaned = sanitize_data_columns(rows)

        self._logger.debug(f"Cleaned: \n{cleaned.to_string()}", separator=self._separator)

        tier_counts: Dict[str, int] = defaultdict(int)

        for row in cleaned.itertuples(index=False):
            rarity = getattr(row, "rarity__1_6")
            usefulness = getattr(row, "usefulness__1_6")
            tier = get_tier_from_rarity_and_use(rarity, usefulness)
            tier_counts[tier.value] += 1
            style      = determine_orb_style(data, tier)
            rules.append(get_tier_currency_rule(self._rule_factory, self._condition_factory, style, row.basetype, tier))

        self._logger.info(f"Tiers:\n{pprint.pformat(tier_counts)}", separator=self._separator)

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
