from typing import Callable, Dict, Any

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder


class CustomSoundHandler(StyleComponentHandler):
    def __init__(self,
                 apply_fn: Callable[[str, int], None],
                 logger: HoornLogger,
                 separator: str) -> None:
        self._apply_fn = apply_fn
        self._logger = logger
        self._separator = separator

    def handle(self, builder: StyleBuilder, sound_dict: Dict[str, Any]) -> bool:
        try:
            file = sound_dict["file"]
            volume = sound_dict["volume"]
            self._apply_fn(file, volume)
            return True
        except KeyError as e:
            self._logger.warning(f"Invalid color key: {e}", separator=self._separator)
            return False
