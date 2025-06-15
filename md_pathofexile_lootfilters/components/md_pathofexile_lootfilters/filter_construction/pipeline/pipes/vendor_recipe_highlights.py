from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import ArmorTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import UNASSOCIATED_WEAPONRY, \
    ASSOCIATED_WEAPONRY
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_style


class HighlightVendorRecipes(IPipe):
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
            "Highlights every vendor recipe during the campaign."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        rarity_conditions = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            keyword=ConditionKeyWord.Rarity,
            values=["Normal", "Magic", "Rare"]
        )
        class_conditions = self._get_base_class_conditions()
        act_conditions = ConditionGroupFactory.between_acts(
            self._condition_factory,
            Act.Act1,
            Act.Act10
        )
        socket_condition = self._condition_factory.create_condition(ConditionKeyWord.Sockets, operator=ConditionOperator.greater_than_or_equal, value="3RGB")

        style = determine_style(data, ItemTier.MidTier3, BaseTypeCategory.vendor_recipes)

        rules = [
            self._rule_factory.get_rule(rule_type=RuleType.SHOW, conditions=act_conditions + rarity_conditions + class_conditions + [socket_condition], style=style)
        ]

        self._register_section(data, rules)

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data

    def _get_base_class_conditions(self) -> List[Condition]:
        """
        Builds conditions matching all Unassociated Equipment classes.
        """
        values = [item.value for item in UNASSOCIATED_WEAPONRY] + [item.value for item in ASSOCIATED_WEAPONRY] + [item.value for _, item in enumerate(ArmorTypeClass)]
        return ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            keyword=ConditionKeyWord.Class,
            values=values,
            operator=ConditionOperator.exact_match
        )

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
