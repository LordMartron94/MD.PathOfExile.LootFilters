from typing import List

import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule


class RuleSection(pydantic.BaseModel):
    heading: str
    description: str
    rules: List[Rule]
