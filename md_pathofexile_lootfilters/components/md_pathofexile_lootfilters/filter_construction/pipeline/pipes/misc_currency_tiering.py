import enum
from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.orb_base_type import OrbBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.utility_base_type import \
    GeneralCurrencyBaseType, SupplyBaseType
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
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_orb_style, determine_currency_style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class AddMiscCurrenciesTiering(IPipe):
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

        for _, currency_base in enumerate(GeneralCurrencyBaseType):
            style, tier = determine_currency_style(data, currency_base)
            rules.append(self._get_rule(style, currency_base, tier))

        for _, currency_base in enumerate(SupplyBaseType):
            style, tier = determine_currency_style(data, currency_base)
            rules.append(self._get_rule(style, currency_base, tier))

        return rules

    def _get_rule(self, style: Style, base: enum.Enum, tier: ItemTier) -> Rule:
        type_condition = self._condition_factory.create_condition(ConditionKeyWord.BaseType, operator=ConditionOperator.exact_match, value=f'"{base.value}"')
        area_conditions = ConditionGroupFactory.between_acts(self._condition_factory, Act.Act1, Act.Act10)

        rule = self._rule_factory.get_rule(
            rule_type=RuleType.SHOW,
            conditions=[type_condition] + area_conditions,
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
