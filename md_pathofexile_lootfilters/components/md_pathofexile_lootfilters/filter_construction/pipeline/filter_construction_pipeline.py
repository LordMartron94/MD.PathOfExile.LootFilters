from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import AbPipeline
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.catch_all import \
    AddCatchAllRules
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.hide_unassociated_class_items import \
    HideUnassociatedClassItems
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.item_progressions import \
    AddItemProgressions
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.jewelry_highlights import \
    AddJewelryHighlights


class FilterConstructionPipeline(AbPipeline):
    def __init__(self, logger: HoornLogger):
        self._pipeline_prefix: str = "FilterConstructionPipeline"

        self._rule_factory: RuleFactory = RuleFactory(logger)
        self._condition_factory: ConditionFactory = ConditionFactory()

        super().__init__(logger, pipeline_descriptor=self._pipeline_prefix)
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def build_pipeline(self):
        self._add_step(HideUnassociatedClassItems(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8100] Unassociated Class-Items"))
        self._add_step(AddItemProgressions(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8200] Item Progressions"))
        self._add_step(AddJewelryHighlights(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8300] Jewelry Highlights"))
        self._add_step(AddCatchAllRules(self._logger, self._rule_factory, self._pipeline_prefix, "[9999] Catch All"))
