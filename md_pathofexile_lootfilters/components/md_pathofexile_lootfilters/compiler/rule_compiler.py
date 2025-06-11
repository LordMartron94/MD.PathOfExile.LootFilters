from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.rendering.renderer import Renderer


class RuleCompiler:
    def __init__(self,
                 renderers: List[Renderer],
                 logger: HoornLogger):
        self._renderers = renderers
        self._logger = logger
        self._separator: str = self.__class__.__name__
        self._logger.trace("Compiler initialized", separator=self._separator)

    def compile(self, rule: Rule) -> str:
        self._logger.debug(f"Compiling rule {rule.rule_type}", separator=self._separator)

        first_line: str = rule.rule_type.value

        if rule.comment is not None:
            first_line += f" # --- {rule.comment}"

        lines: List[str] = [first_line]
        for renderer in self._renderers:
            renderer.render(lines, rule)
        return "\n".join(lines) + "\n"
