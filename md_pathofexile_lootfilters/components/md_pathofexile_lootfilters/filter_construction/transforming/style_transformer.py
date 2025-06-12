from typing import Mapping, Dict, Any, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class StyleTransformer:
    def __init__(self,
                 builder: StyleBuilder,
                 handlers: Mapping[str, StyleComponentHandler],
                 logger: HoornLogger,
                 separator: str) -> None:
        self._builder = builder
        self._handlers = handlers
        self._logger = logger
        self._separator = separator

    def transform(self, raw: Dict[str, Any]) -> Optional[Style]:
        self._builder.reset()
        for key, val in raw.items():
            handler = self._handlers.get(key)
            if handler is None:
                self._logger.warning(f"No handler for style component: {key}", separator=self._separator)
                continue
            if not handler.handle(self._builder, val):
                self._logger.warning(f"Handler failed for: {key}", separator=self._separator)
                return None
        return self._builder.build()
