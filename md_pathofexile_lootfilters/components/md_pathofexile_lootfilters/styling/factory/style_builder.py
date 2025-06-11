from typing import Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_component_factory import \
    StyleComponentFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.minimap_icon import MinimapIcon
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.play_effect import PlayEffect
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral, \
    MinimapShapeLiteral


class StyleBuilder:
    """
    Fluent builder for constructing a Style instance with optional logging.
    """

    def __init__(self, logger: HoornLogger, factory: Optional[StyleComponentFactory] = None):
        self._logger = logger
        self._separator: str = self.__class__.__name__
        self._factory = factory or StyleComponentFactory()

        # optional components
        self._minimap_icon: Optional[MinimapIcon] = None
        self._play_effect: Optional[PlayEffect] = None
        self._custom_alert_sound = None
        self._play_alert_sound = None

        # drop sound toggles
        self._disable_drop_sound: bool = False
        self._enable_drop_sound: bool = False
        self._disable_drop_sound_if_alert_sound: bool = False
        self._enable_drop_sound_if_alert_sound: bool = False

        # required style attributes
        self._background_color = None
        self._border_color = None
        self._text_color = None
        self._font_size: Optional[int] = None

    def with_minimap_icon(
            self,
            size: int = 0,
            color: ColorLiteral = "Red",
            shape: MinimapShapeLiteral = "Star",
    ) -> "StyleBuilder":
        """
        Attach MinimapIcon via factory.
        """
        self._minimap_icon = self._factory.create_minimap_icon(
            size=size,
            color=color,
            shape=shape,
        )
        return self

    def with_play_effect(
            self,
            color: ColorLiteral = "Red",
            temp: bool = False,
    ) -> "StyleBuilder":
        """
        Attach PlayEffect via factory.
        """
        self._play_effect = self._factory.create_play_effect(
            color=color,
            temp=temp,
        )
        return self

    def with_custom_alert_sound(
            self,
            file_name: str,
            volume: int,
            optional: bool = False,
    ) -> "StyleBuilder":
        """
        Attach CustomAlertSound via factory.
        """
        self._custom_alert_sound = self._factory.create_custom_alert_sound(
            file_name=file_name,
            volume=volume,
            optional=optional,
        )
        return self

    def with_play_alert_sound(
            self,
            id: int,
            volume: int,
            positional: bool = False,
    ) -> "StyleBuilder":
        """
        Attach PlayAlertSound via factory.
        """
        self._play_alert_sound = self._factory.create_play_alert_sound(
            id=id,
            volume=volume,
            positional=positional,
        )
        return self

    def disable_drop_sound(self) -> "StyleBuilder":
        """
        Disable default drop sound.
        """
        self._disable_drop_sound = True
        return self

    def enable_drop_sound(self) -> "StyleBuilder":
        """
        Enable default drop sound.
        """
        self._enable_drop_sound = True
        return self

    def disable_drop_sound_if_alert_sound(self) -> "StyleBuilder":
        """
        Disable drop sound when an alert sound is played.
        """
        self._disable_drop_sound_if_alert_sound = True
        return self

    def enable_drop_sound_if_alert_sound(self) -> "StyleBuilder":
        """
        Enable drop sound when an alert sound is played.
        """
        self._enable_drop_sound_if_alert_sound = True
        return self

    def with_background_color(
        self,
        red: int,
        green: int,
        blue: int,
        alpha: int = 240,
    ) -> "StyleBuilder":
        """
        Attach background color via factory.
        """
        self._background_color = self._factory.create_background_color(
            red=red,
            green=green,
            blue=blue,
            alpha=alpha,
        )
        return self

    def with_border_color(
        self,
        red: int,
        green: int,
        blue: int,
        alpha: int = 255,
    ) -> "StyleBuilder":
        """
        Attach border color via factory.
        """
        self._border_color = self._factory.create_border_color(
            red=red,
            green=green,
            blue=blue,
            alpha=alpha,
        )
        return self

    def with_text_color(
        self,
        red: int,
        green: int,
        blue: int,
        alpha: int = 255,
    ) -> "StyleBuilder":
        """
        Attach text color via factory.
        """
        self._text_color = self._factory.create_text_color(
            red=red,
            green=green,
            blue=blue,
            alpha=alpha,
        )
        return self

    def with_font_size(self, font_size: int) -> "StyleBuilder":
        """
        Set font size.
        """
        self._font_size = font_size
        return self

    def reset(self) -> "StyleBuilder":
        """
        Clear all settings for a fresh start.
        """
        self._minimap_icon = None
        self._play_effect = None
        self._custom_alert_sound = None
        self._play_alert_sound = None
        self._disable_drop_sound = False
        self._enable_drop_sound = False
        self._disable_drop_sound_if_alert_sound = False
        self._enable_drop_sound_if_alert_sound = False
        self._background_color = None
        self._border_color = None
        self._text_color = None
        self._font_size = None
        return self

    def build(self, clear_after: bool = False) -> Optional[Style]:
        """
        Construct the Style model if all required fields set. Optionally reset state.
        """
        if not self._is_ready_to_build():
            return None

        style = Style(
            minimap_icon=self._minimap_icon,
            play_effect=self._play_effect,
            play_alert_sound=self._play_alert_sound,
            custom_alert_sound=self._custom_alert_sound,
            disable_drop_sound=self._disable_drop_sound,
            enable_drop_sound=self._enable_drop_sound,
            disable_drop_sound_if_alert_sound=self._disable_drop_sound_if_alert_sound,
            enable_drop_sound_if_alert_sound=self._enable_drop_sound_if_alert_sound,
            background_color=self._background_color,
            border_color=self._border_color,
            text_color=self._text_color,
            font_size=self._font_size,
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
                separator=self._separator,
            )
            return False
        return True
