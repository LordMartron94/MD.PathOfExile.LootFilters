from typing import List

import pandas as pd
import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.style_preset_registry import \
    StylePresetRegistry


class FilterConstructionPipelineContext(pydantic.BaseModel):
    style_preset_registry: StylePresetRegistry
    base_type_data: pd.DataFrame
    uniques_data: pd.DataFrame

    generated_rules: List[RuleSection] = []

    model_config = {
        "arbitrary_types_allowed": True
    }
