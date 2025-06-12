import pprint
from typing import List, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.rendering.condition_renderer import \
    ConditionRenderer
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.rendering.style_renderer import \
    StyleRenderer
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.rule_compiler import RuleCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.utils.keyword_line_adder import \
    KeywordLineAdder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import VERBOSE
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.rule_section import \
    RuleSection
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class FilterCompiler:
    """
    Used to transform rules (with optional nested sub-rules) and styling into lootfilter text,
    now delegating rendering to SOLID-compliant RuleCompiler strategies.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator = self.__class__.__name__
        self._logger.trace("Successfully initialized.", separator=self._separator)

        # Set up renderers and the new RuleCompiler
        keyword_adder = KeywordLineAdder()
        condition_renderer = ConditionRenderer()
        style_renderer = StyleRenderer(keyword_adder)
        self._compiler = RuleCompiler(
            renderers=[condition_renderer, style_renderer],
            logger=logger
        )

    def transform_single_rule(self, rule: Rule) -> str:
        """
        Convert a Rule and its Style into filter text using the injected RuleCompiler.
        """
        # Retain original detailed logging
        self._log_inputs(rule, rule.style)
        return self._compiler.compile(rule)

    def transform_batch_rule_sections(
            self,
            rule_sections: List[RuleSection]
    ) -> List[str]:
        output: List[str] = []

        for rule_section in rule_sections:
            output.append(f"# ===== {rule_section.heading} =====")
            output.append(f"# {rule_section.description}")

            for rule in rule_section.rules:
                output.append(self.transform_single_rule(rule))

        return output

    def _log_inputs(self, block: Rule, style: Optional[Style]) -> None:
        if not VERBOSE:
            return

        block_json = pprint.pformat(block.model_dump(mode='json'))
        style_json = pprint.pformat(style.model_dump(mode='json')) if style else None
        self._logger.debug(
            f"Transforming block:\n{block_json}\nStyle:\n{style_json}",
            separator=self._separator
        )
