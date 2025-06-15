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
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.appending.strategy.game_rarity_designation import \
    GameRarityAppender
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.constructing.strategy.game_rarity_designation_strategy import \
    GameRarityDesignationMappingStrategy
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.tier_mapping.tier_rule_applier import \
    TierRuleApplier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    filter_rows_by_category, BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.print_tiers import \
    log_tiers
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.tier_mapping_sorter import \
    TierMappingSorter


class AddJewelryHighlights(IPipe):
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

    def _get_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        rules = []

        jewelry = filter_rows_by_category([BaseTypeCategory.rings, BaseTypeCategory.amulets], data.base_type_data)
        tier_counts: Dict[str, int] = defaultdict(int)

        self._tier_rule_applier.apply(
            jewelry,
            data,
            BaseTypeCategory.rings,
            tier_counts,
            rules,
            mapping_strategy=GameRarityDesignationMappingStrategy(),
            appender_strategy=GameRarityAppender(self._rule_factory, self._condition_factory,
                                                 act_mappings={
                                                     "Normal": (Act.Act1, Act.Act1),
                                                     "Magic": (Act.Act1, Act.Act2),
                                                     "Rare": (Act.Act1, Act.Act10),
                                                 }),
            base_type_accessor="basetype",
            accessors={
                "normal_accessor": "normal_tier",
                "magic_accessor": "magic_tier",
                "rare_accessor": "rare_tier",
            }
        )

        # Hide rule
        act_conditions = ConditionGroupFactory.between_acts(self._condition_factory, Act.Act1, Act.Act10)
        rarity_conditions = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            ConditionKeyWord.Rarity,
            operator=ConditionOperator.exact_match,
            values=["Normal", "Magic", "Rare"]
        )

        classes = ["Rings", "Amulets"]

        class_conditions = ConditionGroupFactory.from_exact_values(
            self._condition_factory,
            ConditionKeyWord.Class,
            operator=ConditionOperator.exact_match,
            values=classes
        )

        rules.append(self._rule_factory.get_rule(RuleType.HIDE, conditions=class_conditions + rarity_conditions + act_conditions, style=None))

        log_tiers(self._logger, tier_counts, self._separator, "Jewelry")

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
