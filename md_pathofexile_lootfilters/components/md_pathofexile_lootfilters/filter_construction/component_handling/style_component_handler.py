from abc import ABC, abstractmethod
from typing import Any

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder


class StyleComponentHandler(ABC):
    @abstractmethod
    def handle(self, builder: StyleBuilder, data: Any) -> bool:
        """
        Apply `data` to the builder. Return True if successful.
        """
        ...
