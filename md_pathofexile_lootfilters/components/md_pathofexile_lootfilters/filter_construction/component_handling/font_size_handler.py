from typing import Any

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder


class FontSizeHandler(StyleComponentHandler):
    def handle(self, builder: StyleBuilder, size: Any) -> bool:
        if not isinstance(size, int):
            return False
        builder.with_font_size(size)
        return True
