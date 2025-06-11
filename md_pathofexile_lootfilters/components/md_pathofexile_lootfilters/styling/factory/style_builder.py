from typing import Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_component_factory import \
    StyleComponentFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.color import Color
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.minimap_icon import MinimapIcon
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.play_effect import PlayEffect
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral, \
    MinimapShapeLiteral


class StyleBuilder:
    def __init__(self, logger: HoornLogger, factory: Optional[StyleComponentFactory] = None):
        """
        Initialize the builder with a StyleComponentFactory instance (or create one by default).
        """
        self._logger = logger
        self._separator: str = self.__class__.__name__

        self._factory = factory or StyleComponentFactory()
        self._minimap_icon: Optional[MinimapIcon] = None
        self._play_effect: Optional[PlayEffect] = None
        self._background_color: Optional[Color] = None
        self._border_color: Optional[Color] = None
        self._text_color: Optional[Color] = None
        self._font_size: Optional[int] = None

    def with_minimap_icon(
            self,
            size: int = 0,
            color: ColorLiteral = "Red",
            shape: MinimapShapeLiteral = "Star"
    ) -> "StyleBuilder":
        """
        Attach a MinimapIcon to the style using the component factory.
        """
        self._minimap_icon = self._factory.create_minimap_icon(
            size=size,
            color=color,
            shape=shape
        )
        return self

    def with_play_effect(
            self,
            color: ColorLiteral = "Red",
            temp: bool = False
    ) -> "StyleBuilder":
        """
        Attach a PlayEffect to the style using the component factory.
        """
        self._play_effect = self._factory.create_play_effect(
            color=color,
            temp=temp
        )
        return self

    def with_background_color(
            self,
            red: int,
            green: int,
            blue: int,
            alpha: int = 240
    ) -> "StyleBuilder":
        """
        Attach a background Color to the style using the component factory.
        """
        self._background_color = self._factory.create_background_color(
            red=red,
            green=green,
            blue=blue,
            alpha=alpha
        )
        return self

    def with_border_color(
            self,
            red: int,
            green: int,
            blue: int,
            alpha: int = 255
    ) -> "StyleBuilder":
        """
        Attach a border Color to the style using the component factory.
        """
        self._border_color = self._factory.create_border_color(
            red=red,
            green=green,
            blue=blue,
            alpha=alpha
        )
        return self

    def with_text_color(
            self,
            red: int,
            green: int,
            blue: int,
            alpha: int = 255
    ) -> "StyleBuilder":
        """
        Attach a text Color to the style using the component factory.
        """
        self._text_color = self._factory.create_text_color(
            red=red,
            green=green,
            blue=blue,
            alpha=alpha
        )
        return self

    def with_font_size(self, font_size: int) -> "StyleBuilder":
        """
        Set the required font size for the style.
        """
        self._font_size = font_size
        return self

    def reset(self) -> "StyleBuilder":
        """
        Clear all the accumulated settings so this builder can be reused from scratch.
        """
        self._minimap_icon = None
        self._play_effect = None
        self._background_color = None
        self._border_color = None
        self._text_color = None
        self._font_size = None
        return self

    def build(self, clear_after: bool = False) -> Optional[Style]:
        """
        Build the Style (and optionally reset the builder for reuse).
        """

        if not self._is_ready_to_build():
            return None

        style = Style(
            minimap_icon=self._minimap_icon,
            play_effect=self._play_effect,
            background_color=self._background_color,
            border_color=self._border_color,
            text_color=self._text_color,
            font_size=self._font_size
        )

        if clear_after:
            self.reset()

        return style

    def _is_ready_to_build(self) -> bool:
        required = {
            "font_size": self._font_size,
            "text_color": self._text_color,
            "border_color": self._border_color,
            "background_color": self._background_color,
        }
        missing = [name for name, val in required.items() if val is None]
        if missing:
            self._logger.warning(
                f"Missing required attributes: {', '.join(missing)}",
                separator=self._separator
            )
            return False
        return True
