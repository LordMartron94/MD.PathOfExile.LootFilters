from typing import Dict, Tuple

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class StylePresetRegistry:
    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__

        self._style_builder: StyleBuilder = StyleBuilder(logger)
        self._lookup: Dict[(ItemGroup, ItemTier), Style] = {}
        self._initialize_lookup()

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def get_style(self, item_group: ItemGroup, item_tier: ItemTier) -> Style:
        key: Tuple[ItemGroup, ItemTier] = (item_group, item_tier)

        style: Style = self._lookup.get(key, None)

        if style is None:
            self._logger.warning(f"No style found for group {item_group.value} tier {item_tier.value}. Returning error style.", separator=self._separator)
            return self._get_error_style()

        return style

    def _initialize_lookup(self) -> None:
        self._lookup[(ItemGroup.CatchAll, ItemTier.NoTier)] = self._get_catch_all_style()
        self._lookup[(ItemGroup.EarlyWeaponry, ItemTier.NoTier)] = self._get_early_weaponry_style()
        self._lookup[(ItemGroup.Weaponry, ItemTier.Tier1)] = self._get_main_weaponry_style_t1()
        self._lookup[(ItemGroup.Weaponry, ItemTier.Tier2)] = self._get_main_weaponry_style_t2()
        self._lookup[(ItemGroup.Weaponry, ItemTier.Tier3)] = self._get_main_weaponry_style_t3()

    def _get_main_weaponry_style_t1(self) -> Style:
        style = (
            #192 155 0 255
            self._style_builder
            .with_background_color(40, 40, 40, 255)
            .with_border_color(192, 155, 0, 255)
            .with_text_color(192, 155, 0, 255)
            .with_font_size(35)
            .build(clear_after=True)
        )
        return style or self._get_error_style()

    def _get_main_weaponry_style_t2(self) -> Style:
        style = (
            self._style_builder
            .with_background_color(40, 40, 40, 255)
            .with_border_color(120, 160, 220, 255)
            .with_text_color(120, 160, 220, 255)
            .with_font_size(27)
            .build(clear_after=True)
        )
        return style or self._get_error_style()

    def _get_main_weaponry_style_t3(self) -> Style:
        style = (
            self._style_builder
            .with_background_color(40, 40, 40, 255)
            .with_border_color(150, 100,  60, 255)
            .with_text_color(150, 100,  60, 255)
            .with_font_size(20)
            .build(clear_after=True)
        )
        return style or self._get_error_style()

    def _get_early_weaponry_style(self) -> Style:
        style = (self._style_builder
                 .with_background_color(40, 30, 20, 180)
                 .with_border_color(100, 100, 90, 255)
                 .with_text_color(230, 220, 200, 255)
                 .with_font_size(25)
                 .build(clear_after=True))

        if style is None:
            return self._get_error_style()

        return style

    def _get_catch_all_style(self) -> Style:
        style = (self._style_builder
         .with_background_color(255, 0, 255, 255)
         .with_border_color(0, 255, 255, 255)
         .with_text_color(0, 0, 0, 255)
         .with_font_size(45)).build(clear_after=True)

        if style is None:
            return self._get_error_style()

        return style

    def _get_error_style(self) -> Style:
        style = (self._style_builder
                .with_background_color(255, 0, 0, 255)
                .with_border_color(0, 0, 0, 255)
                .with_text_color(255, 255, 255, 255)
                .with_font_size(45)).build(clear_after=True)

        if style is None:
            raise ValueError("Cannot create error style! Fix your code you dumb-ass!")

        return style
