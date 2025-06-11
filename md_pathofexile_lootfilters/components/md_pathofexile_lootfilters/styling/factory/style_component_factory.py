from typing import Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.color import Color
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.minimap_icon import MinimapIcon
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.play_effect import PlayEffect
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.custom_alert_sound import CustomAlertSound
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.play_alert_sound import PlayAlertSound
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral, MinimapShapeLiteral


class StyleComponentFactory:
    """
    Factory for creating styling-related components with sensible defaults and validation.
    """

    @staticmethod
    def create_minimap_icon(
            size: int = 0,
            color: ColorLiteral = "Red",
            shape: MinimapShapeLiteral = "Star"
    ) -> MinimapIcon:
        """
        Create a MinimapIcon with the given size, color and shape.

        :param size: icon size, between 0 and 2 inclusive
        :param color: one of the allowed colour literals
        :param shape: one of the allowed shape literals
        :return: a validated MinimapIcon instance
        """
        return MinimapIcon(size=size, colour=color, shape=shape)

    @staticmethod
    def create_play_effect(
            color: ColorLiteral = "Red",
            temp: Optional[bool] = False
    ) -> PlayEffect:
        """
        Create a PlayEffect with the given color and temporary flag.

        :param color: one of the allowed color literals
        :param temp: whether the effect is temporary
        :return: a validated PlayEffect instance
        """
        return PlayEffect(colour=color, temp=temp)

    @staticmethod
    def create_background_color(
            red: int,
            green: int,
            blue: int,
            alpha: int = 240
    ) -> Color:
        """
        Create a Color for backgrounds with a default alpha of 240.

        :param red: red component (0-255)
        :param green: green component (0-255)
        :param blue: blue component (0-255)
        :param alpha: alpha component (0-255), defaults to 240
        :return: a validated Color instance
        """
        return Color(red=red, green=green, blue=blue, alpha=alpha)

    @staticmethod
    def create_border_color(
            red: int,
            green: int,
            blue: int,
            alpha: int = 255
    ) -> Color:
        """
        Create a Color for borders with a default alpha of 255.

        :param red: red component (0-255)
        :param green: green component (0-255)
        :param blue: blue component (0-255)
        :param alpha: alpha component (0-255), defaults to 255
        :return: a validated Color instance
        """
        return Color(red=red, green=green, blue=blue, alpha=alpha)

    @staticmethod
    def create_text_color(
            red: int,
            green: int,
            blue: int,
            alpha: int = 255
    ) -> Color:
        """
        Create a Color for text with a default alpha of 255.

        :param red: red component (0-255)
        :param green: green component (0-255)
        :param blue: blue component (0-255)
        :param alpha: alpha component (0-255), defaults to 255
        :return: a validated Color instance
        """
        return Color(red=red, green=green, blue=blue, alpha=alpha)

    @staticmethod
    def create_custom_alert_sound(
            file_name: str,
            volume: int,
            optional: Optional[bool] = False
    ) -> CustomAlertSound:
        """
        Create a CustomAlertSound for alerting with a sound file.

        :param file_name: name of the alert sound file
        :param volume: playback volume (0-300)
        :param optional: whether this sound is optional
        :return: a validated CustomAlertSound instance
        """
        return CustomAlertSound(file_name=file_name, volume=volume, optional=optional)

    @staticmethod
    def create_play_alert_sound(
            id: int,
            volume: int,
            positional: Optional[bool] = False
    ) -> PlayAlertSound:
        """
        Create a PlayAlertSound to trigger an in-game alert.

        :param id: alert sound ID (1-16)
        :param volume: playback volume (0-300)
        :param positional: whether the sound should be positional
        :return: a validated PlayAlertSound instance
        """
        return PlayAlertSound(id=id, volume=volume, positional=positional)
