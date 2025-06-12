import traceback
from pathlib import Path
from typing import List

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.compiler import FilterCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import OUTPUT_DIRECTORIES
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.filter_construction_pipeline import \
    FilterConstructionPipeline
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.style_preset_registry import \
    StylePresetRegistry


class FilterConstructor:
    """
    High-Level API/Class to handle the construction of loot filters.
    """

    def __init__(self, logger: HoornLogger):
        self._logger = logger
        self._separator: str = self.__class__.__name__

        self._compiler: FilterCompiler = FilterCompiler(logger)
        _style_preset_registry: StylePresetRegistry = StylePresetRegistry(logger)

        self._pipeline = FilterConstructionPipeline(logger)
        self._pipeline.build_pipeline()

        self._pipeline_context = FilterConstructionPipelineContext(
            style_preset_registry=_style_preset_registry
        )

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def construct_filter(self) -> None:
        context: FilterConstructionPipelineContext = self._pipeline.flow(data=self._pipeline_context)
        transformed_str: List[str] = self._compiler.transform_batch_rule_sections(context.generated_rules)

        for output_dir in OUTPUT_DIRECTORIES:
            filter_path: Path = output_dir / "MD.TestFilter.filter"

            try:
                with open(filter_path, "w") as filter_file:
                    filter_file.write('\n'.join(transformed_str))
            except Exception as e:
                tb = traceback.format_exc()
                self._logger.error(f"Something went wrong while outputting to \"{filter_path}\". Exception: \"{e}\"\n{tb}", separator=self._separator)

            self._logger.info(f"Output written to \"{filter_path}\".", separator=self._separator)
