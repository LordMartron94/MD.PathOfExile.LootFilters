from typing import Optional

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.color import Color
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.minimap_icon import MinimapIcon
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.play_effect import PlayEffect
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral, MinimapShapeLiteral


class StyleComponentFactory:
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
