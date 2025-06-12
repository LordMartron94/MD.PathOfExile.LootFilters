from typing import Dict, Any, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.color_handler import \
    ColorHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.font_size_handler import \
    FontSizeHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.component_handling.style_component_handler import \
    StyleComponentHandler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.loading.style_config_loader import \
    StyleConfigLoader
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.transforming.style_transformer import \
    StyleTransformer
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class StyleTemplateRetriever:
    def __init__(
            self,
            logger: HoornLogger,
            config_loader: StyleConfigLoader,
            style_builder: StyleBuilder
    ) -> None:
        self._logger = logger
        self._separator = self.__class__.__name__

        config = config_loader.load()
        self._item_group_styles: Dict[str, Dict[str, Any]] = config["item_groups"]
        self._item_tier_styles: Dict[str, Dict[str, Any]] = config["item_tiers"]
        self._error_raw: Dict[str, Any] = config["error"]
        self._catch_all_raw: Dict[str, Any] = config["catch_all"]

        # noinspection PyTypeChecker
        handlers: Dict[str, StyleComponentHandler] = {
            "background_color": ColorHandler(style_builder.with_background_color, logger, self._separator),
            "border_color":     ColorHandler(style_builder.with_border_color,    logger, self._separator),
            "text_color":       ColorHandler(style_builder.with_text_color,      logger, self._separator),
            "font_size":        FontSizeHandler(),
        }

        self._transformer = StyleTransformer(style_builder, handlers, logger, self._separator)

        # Pre-build error and catch-all styles
        self._error_style = self._transformer.transform(self._error_raw) or self._fatal("error")
        self._catch_all_style = self._transformer.transform(self._catch_all_raw) or self._fatal("catch_all")

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def get_style(self, group: ItemGroup, tier: ItemTier) -> Optional[Style]:
        if group is ItemGroup.CatchAll:
            return self._catch_all_style

        raw_group = self._item_group_styles.get(group.value)
        raw_tier = self._item_tier_styles.get(tier.value)

        if raw_group is None or raw_tier is None:
            self._logger.warning(f"Missing style data for group={group.value}, tier={tier.value}", separator=self._separator)
            return None

        merged = {**raw_group, **raw_tier}
        return self._transformer.transform(merged)

    def get_error_style(self) -> Style:
        return self._error_style

    def _fatal(self, which: str) -> Style:
        msg = f"Could not build {which} style!"
        self._logger.error(msg, separator=self._separator)
        raise RuntimeError(msg)
