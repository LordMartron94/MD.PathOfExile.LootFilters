import traceback
from pathlib import Path

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import BlockType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.compiler import FilterCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import BlockFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.block import Block
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import OUTPUT_DIRECTORIES
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.style_preset_registry import \
    StylePresetRegistry
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


class FilterConstructor:
    """
    High-Level API/Class to handle the construction of loot filters.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__

        self._block_factory: BlockFactory = BlockFactory(logger)
        self._compiler: FilterCompiler = FilterCompiler(logger)
        self._style_preset_registry: StylePresetRegistry = StylePresetRegistry(logger)

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def construct_filter(self) -> None:
        catch_all_block: Block = self._block_factory.get_catch_all_block(BlockType.SHOW)

        style: Style = self._style_preset_registry.get_style(ItemGroup.CatchAll, ItemTier.NoTier)

        transformed_str: str = self._compiler.transform_single_block(catch_all_block, style)

        for output_dir in OUTPUT_DIRECTORIES:
            filter_path: Path = output_dir / "MD.TestFilter.filter"

            try:
                with open(filter_path, "w") as filter_file:
                    filter_file.write(transformed_str)
            except Exception as e:
                tb = traceback.format_exc()
                self._logger.error(f"Something went wrong while outputting to \"{filter_path}\". Exception: \"{e}\"\n{tb}", separator=self._separator)

            self._logger.info(f"Output written to \"{filter_path}\".", separator=self._separator)
