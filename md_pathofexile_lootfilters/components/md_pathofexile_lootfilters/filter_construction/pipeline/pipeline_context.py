from typing import List

import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.style_preset_registry import \
    StylePresetRegistry


class FilterConstructionPipelineContext(pydantic.BaseModel):
    rule_factory: RuleFactory
    condition_factory: ConditionFactory
    style_preset_registry: StylePresetRegistry

    generated_rules: List[RuleSection] = []

    model_config = {
        "arbitrary_types_allowed": True
    }
