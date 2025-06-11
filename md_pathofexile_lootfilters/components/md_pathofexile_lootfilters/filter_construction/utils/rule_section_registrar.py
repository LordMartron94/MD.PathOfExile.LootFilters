from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext


class RuleSectionRegistrar:
    @staticmethod
    def register(
            ctx: FilterConstructionPipelineContext,
            heading: str,
            description: str,
            rules: List[Rule]
    ) -> None:
        ctx.generated_rules.append(RuleSection(heading=heading, description=description, rules=rules))
