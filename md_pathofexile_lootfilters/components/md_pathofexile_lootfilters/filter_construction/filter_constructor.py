import pprint
import traceback
from pathlib import Path
from typing import List

import numpy as np
import pandas

from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.compiler import FilterCompiler
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import OUTPUT_DIRECTORIES, FILTER_NAME, \
    CONFIG_DIR
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

    def __init__(self, logger: HoornLogger, valid_base_types: List[str]):
        self._logger = logger
        self._separator: str = self.__class__.__name__

        self._compiler: FilterCompiler = FilterCompiler(logger)
        self._style_preset_registry: StylePresetRegistry = StylePresetRegistry(logger)
        self._valid_base_types: List[str] = valid_base_types

        self._pipeline = FilterConstructionPipeline(logger)
        self._pipeline.build_pipeline()

        self._load_data()

        self._logger.trace("Successfully initialized.", separator=self._separator)

    def _load_data(self):
        base_type_data = pandas.read_csv(
            CONFIG_DIR / "base_types.csv",
            keep_default_na=True)

        base_type_data = base_type_data.astype(object)
        base_type_data = base_type_data.replace({ np.nan: None })

        uniques_data = pandas.read_csv(
            CONFIG_DIR / "uniques.csv"
        )

        skill_gems_data = pandas.read_csv(
            CONFIG_DIR / "skill_gems.csv"
        )

        self._pipeline_context = FilterConstructionPipelineContext(
            style_preset_registry=self._style_preset_registry,
            base_type_data=base_type_data,
            uniques_data = uniques_data,
            skill_gems_data=skill_gems_data,
            valid_base_types_unique_and_gem=self._valid_base_types
        )

        self._logger.debug(f"Dataframe:\n{pprint.pformat(self._pipeline_context.base_type_data)}", separator=self._separator)

    def reload_data(self) -> None:
        self._load_data()

    def construct_filter(self) -> None:
        context: FilterConstructionPipelineContext = self._pipeline.flow(data=self._pipeline_context)
        transformed_str: List[str] = self._compiler.transform_batch_rule_sections(context.generated_rules)

        for output_dir in OUTPUT_DIRECTORIES:
            filter_path: Path = output_dir / FILTER_NAME

            try:
                with open(filter_path, "w", encoding="utf-8") as filter_file:
                    filter_file.write('\n'.join(transformed_str))
            except Exception as e:
                tb = traceback.format_exc()
                self._logger.error(f"Something went wrong while outputting to \"{filter_path}\". Exception: \"{e}\"\n{tb}", separator=self._separator)

            self._logger.info(f"Output written to \"{filter_path}\".", separator=self._separator)
