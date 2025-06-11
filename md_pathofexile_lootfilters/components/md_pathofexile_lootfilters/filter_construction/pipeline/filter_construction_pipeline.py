from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import AbPipeline
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.catch_all import \
    AddCatchAllRules
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.class_weapons import \
    AddClassWeaponsRules


class FilterConstructionPipeline(AbPipeline):
    def __init__(self, logger: HoornLogger):
        self._pipeline_prefix: str = "FilterConstructionPipeline"

        super().__init__(logger, pipeline_descriptor=self._pipeline_prefix)
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def build_pipeline(self):
        self._add_step(AddClassWeaponsRules(self._logger, self._pipeline_prefix, "[1000] Class Associated Weaponry"))
        self._add_step(AddCatchAllRules(self._logger, self._pipeline_prefix, "[9999] Catch All"))
