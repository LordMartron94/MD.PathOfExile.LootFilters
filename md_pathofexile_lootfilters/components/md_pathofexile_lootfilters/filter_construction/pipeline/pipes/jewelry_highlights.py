import pprint
from collections import defaultdict
from typing import List, Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
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
    ItemTier, parse_tier_value
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    filter_rows_by_category, BaseTypeCategory, sanitize_data_columns
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class AddJewelryHighlights(IPipe):
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
            "Highlights the rings and amulets associated with our build."
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

        jewelry = filter_rows_by_category([BaseTypeCategory.rings, BaseTypeCategory.amulets], data.base_type_data)
        cleaned = sanitize_data_columns(jewelry)

        tier_counts: Dict[str, int] = defaultdict(int)

        for rarity in ("Normal", "Magic", "Rare"):
            col = f"{rarity}_Tier".lower()
            for row in cleaned.itertuples(index=False):
                tier_value = getattr(row, col)
                tier       = parse_tier_value(tier_value)
                tier_counts[tier.value] += 1
                style      = determine_style(data, tier, BaseTypeCategory.rings)  # either rings or amulets here is fine.
                rules.append(self._get_rule(style, row.basetype, rarity, tier))

        self._logger.info(f"Tiers:\n{pprint.pformat(tier_counts)}", separator=self._separator)

        return rules

    def _get_rule(self, style: Style, base: str, rarity: str, tier: ItemTier) -> Rule:
        type_condition = self._condition_factory.create_condition(ConditionKeyWord.BaseType, operator=ConditionOperator.exact_match, value=f'"{base}"')
        rarity_condition = self._condition_factory.create_condition(ConditionKeyWord.Rarity, operator=ConditionOperator.exact_match, value=f'"{rarity}"')

        if rarity == "Normal":
            area_conditions = ConditionGroupFactory.between_acts(self._condition_factory, Act.Act1, Act.Act1)
        elif rarity == "Magic":
            area_conditions = ConditionGroupFactory.between_acts(self._condition_factory, Act.Act1, Act.Act2)
        else: area_conditions = ConditionGroupFactory.between_acts(self._condition_factory, Act.Act1, Act.Act10)

        rule = self._rule_factory.get_rule(
            rule_type=RuleType.SHOW,
            conditions=[type_condition, rarity_condition] + area_conditions,
            style=style,
        )

        rule.comment = f"Tier: \"{tier.value}\""

        return rule

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
