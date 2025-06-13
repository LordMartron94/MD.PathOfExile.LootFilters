from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.utils import parse_literal
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral


class EffectHandler(StyleComponentHandler):
    def __init__(self, logger: HoornLogger, separator: str):
        self._logger = logger
        self._separator = separator

    def handle(self, builder: StyleBuilder, effect_color: str) -> bool:
        try:
            color: ColorLiteral = parse_literal(effect_color, ColorLiteral)
            builder.with_play_effect(
                color
            )
            return True
        except Exception as e:
            self._logger.error(f"There was an error adding the effect: {e}", separator=self._separator)
            return False
