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
    ConditionOperator, Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import ArmorTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import UNASSOCIATED_WEAPONRY, \
    ASSOCIATED_WEAPONRY
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    bump_tier, ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    get_weaponry_and_equipment_tier, get_weapon_style_from_tier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class HighlightImportantItems(IPipe):
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

        self._section_heading = section_heading
        self._section_description = (
            "Highlights important equipment within the campaign (i.e., 4 links)."
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        class_conditions = self._get_base_class_conditions()
        act_conditions = ConditionGroupFactory.between_acts(self._condition_factory, Act.Act2, Act.Act10)

        rules = self._get_rules(data, class_conditions, act_conditions)

        self._register_section(data, rules)

        self._logger.info(
            f"Added section '{self._section_heading}' successfully!",
            separator=self._separator
        )
        return data

    def _get_rules(self,
                   data: FilterConstructionPipelineContext,
                   class_conditions: List[Condition],
                   act_conditions: List[Condition]) -> List[Rule]:
        rules = []

        mapping = {
            3: 1,
            4: 2,
            6: 3
        }
        items: Dict[ItemTier, List[Rule]] = defaultdict(list)

        for rarity in ("Normal", "Magic", "Rare"):
            rarity_condition = self._condition_factory.create_condition(ConditionKeyWord.Rarity, operator=ConditionOperator.exact_match, value=f'"{rarity}"')
            base_tier = get_weaponry_and_equipment_tier(rarity)

            for link_amount in sorted(mapping, reverse=True):
                socket_condition = self._condition_factory.create_condition(ConditionKeyWord.SocketGroup, ConditionOperator.greater_than_or_equal, value=link_amount)
                bump_amount = mapping[link_amount]
                tier = bump_tier(base_tier, bump_amount)
                style = get_weapon_style_from_tier(data, tier)
                rule = self._rule_factory.get_rule(rule_type=RuleType.SHOW, conditions=class_conditions + [rarity_condition, socket_condition] + act_conditions, style=style)
                rule.comment = f"Tier: {tier.value}"

                items[tier].append(rule)

        sorted_items = self._tier_mapping_sorter.sort(items)

        for _, tier_rules in sorted_items:
            rules.extend(tier_rules)

        return rules

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
