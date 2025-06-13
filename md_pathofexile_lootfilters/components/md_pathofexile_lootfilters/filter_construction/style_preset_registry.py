from pathlib import Path
from typing import Dict, Tuple, Optional

from md_pathofexile_lootfilters.components.md_common_python.py_common.json_storage import JsonStorageHandler
from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import CONFIG_DIR
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.loading.json_config_loader import \
    JsonStyleConfigLoader
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.style_template_retriever import \
    StyleTemplateRetriever
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.factory.style_builder import StyleBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class StylePresetRegistry:
    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__

        _style_builder: StyleBuilder = StyleBuilder(logger)

        _styles_path: Path = CONFIG_DIR / "styles.json"
        _config_loader: JsonStyleConfigLoader = JsonStyleConfigLoader(JsonStorageHandler(logger, _styles_path))
        self._style_template_retriever: StyleTemplateRetriever = StyleTemplateRetriever(logger, _config_loader, _style_builder)

        self._lookup: Dict[(ItemGroup, ItemTier), Style] = {}
        self._initialize_lookup()

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def get_style(self, item_group: ItemGroup, item_tier: ItemTier) -> Style:
        key: Tuple[ItemGroup, ItemTier] = (item_group, item_tier)

        style: Style = self._lookup.get(key, None)

        if style is None:
            self._logger.warning(f"No style found for group {item_group.value} tier {item_tier.value}. Returning error style.", separator=self._separator)
            return self._style_template_retriever.get_error_style()

        return style

    def _initialize_lookup(self) -> None:
        for _, item_group in enumerate(ItemGroup):
            for _, item_tier in enumerate(ItemTier):
                style: Optional[Style] = self._style_template_retriever.get_style(item_group, item_tier)
                self._lookup[(item_group, item_tier)] = style
