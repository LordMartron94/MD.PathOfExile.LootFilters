from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.rendering.renderer import Renderer


class ConditionRenderer(Renderer):
    def render(self, lines: List[str], rule: Rule) -> None:
        for cond in rule.conditions:
            op = f"{cond.operator.value} " if cond.operator else ""
            token = f"{cond.keyword.value} {op}{cond.value}".strip()
            lines.append(f"\t{token}")
