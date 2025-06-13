from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.belt_progression_builder import \
    BeltProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.body_armor_progression_builder import \
    BodyArmorProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.boot_progression_builder import \
    BootProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.flask_progression_builder import \
    FlaskProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.glove_progression_builder import \
    GloveProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.helmet_progression_builder import \
    HelmetProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.sceptre_progression_builder import \
    SceptreProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.shield_progression_builder import \
    ShieldProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import (
    FilterConstructionPipelineContext
)


class AddItemProgressions(IPipe):
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

        # Weaponry
        self._sceptre_progression: SceptreProgressionBuilder = SceptreProgressionBuilder(condition_factory, rule_factory)
        self._shield_progression: ShieldProgressionBuilder = ShieldProgressionBuilder(condition_factory, rule_factory)

        # Main Equipment
        self._body_armor_progression: BodyArmorProgressionBuilder = BodyArmorProgressionBuilder(condition_factory, rule_factory)
        self._helmet_progression: HelmetProgressionBuilder = HelmetProgressionBuilder(condition_factory, rule_factory)
        self._boot_progression: BootProgressionBuilder = BootProgressionBuilder(condition_factory, rule_factory)
        self._glove_progression: GloveProgressionBuilder = GloveProgressionBuilder(condition_factory, rule_factory)
        self._belt_progression: BeltProgressionBuilder = BeltProgressionBuilder(condition_factory, rule_factory)

        # Other
        self._flask_progression: FlaskProgressionBuilder = FlaskProgressionBuilder(condition_factory, rule_factory)

        self._section_heading = section_heading
        self._section_description = (
            "Builds all the item progressions for the campaign. (everything shown in act 1; normals and magics hidden beyond the first act)"
        )

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        rules = []

        # Weaponry
        rules.extend(self._sceptre_progression.get_progression_rules(data))
        rules.extend(self._shield_progression.get_progression_rules(data))

        # Main Equipment
        rules.extend(self._body_armor_progression.get_progression_rules(data))
        rules.extend(self._helmet_progression.get_progression_rules(data))
        rules.extend(self._boot_progression.get_progression_rules(data))
        rules.extend(self._glove_progression.get_progression_rules(data))
        rules.extend(self._belt_progression.get_progression_rules(data))

        # Other
        rules.extend(self._flask_progression.get_progression_rules(data))

        self._register_section(data, rules)

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
