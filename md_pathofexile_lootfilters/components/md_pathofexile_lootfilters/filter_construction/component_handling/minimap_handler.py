from typing import Dict

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.utils import parse_literal
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import MinimapShapeLiteral, \
    ColorLiteral


class MinimapHandler(StyleComponentHandler):
    def __init__(self, logger: HoornLogger, separator: str):
        self._logger = logger
        self._separator = separator

    def handle(self, builder: StyleBuilder, minimap_dict: Dict) -> bool:
        try:
            shape: str = minimap_dict["shape"]
            shape: MinimapShapeLiteral = parse_literal(shape, MinimapShapeLiteral)

            color: str = minimap_dict["color"]
            color: ColorLiteral = parse_literal(color, ColorLiteral)

            size = minimap_dict["size"]
            size = 2 if size == "small" else 1 if size == "medium" else 0 if size == "large" else 3

            if size == 3:
                raise RuntimeError("Size has to be 0-2")

            builder.with_minimap_icon(
                size=size,
                color=color,
                shape=shape,
            )

            return True
        except KeyError as e:
            self._logger.warning(f"Invalid color key: {e}", separator=self._separator)
            return False
