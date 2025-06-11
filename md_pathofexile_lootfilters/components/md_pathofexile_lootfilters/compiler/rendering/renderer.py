from abc import ABC, abstractmethod
from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule


class Renderer(ABC):
    @abstractmethod
    def render(self, lines: List[str], rule: Rule) -> None:
        """Append the relevant lines for this aspect to `lines`."""
        pass
