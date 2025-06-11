from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import IPipe
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext


class AddCatchAllRules(IPipe):
    def __init__(self, logger: HoornLogger, pipeline_prefix: str, section_heading: str):
        self._logger = logger
        self._separator: str = pipeline_prefix + "." + self.__class__.__name__

        self._section_heading = section_heading
        self._section_description: str = "Catches any item not processed by earlier rules. For debugging and development."

    def flow(self, data: FilterConstructionPipelineContext) -> FilterConstructionPipelineContext:
        catch_all_block: Rule = data.rule_factory.get_catch_all_block(RuleType.SHOW)
        catch_all_block.style = data.style_preset_registry.get_style(ItemGroup.CatchAll, ItemTier.NoTier)
        catch_all_block.comment = "Catches everything not captured earlier (above)."

        rule_section: RuleSection = RuleSection(
            heading=self._section_heading,
            description=self._section_description,
            rules=[catch_all_block]
        )

        data.generated_rules.append(rule_section)

        self._logger.info(f"Successfully added {self._section_heading} section!", separator=self._separator)

        return data
