from typing import Callable, Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder


class ColorHandler(StyleComponentHandler):
    def __init__(self,
                 apply_fn: Callable[[int, int, int, int], None],
                 logger: HoornLogger,
                 separator: str) -> None:
        self._apply_fn = apply_fn
        self._logger = logger
        self._separator = separator

    def handle(self, builder: StyleBuilder, color_dict: Dict[str, int]) -> bool:
        try:
            r = color_dict["red"]
            g = color_dict["green"]
            b = color_dict["blue"]
            a = color_dict["alpha"]
            self._apply_fn(r, g, b, a)
            return True
        except KeyError as e:
            self._logger.warning(f"Invalid color key: {e}", separator=self._separator)
            return False
