from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLogger
from md_pathofexile_lootfilters.components.md_common_python.py_common.patterns import AbPipeline
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.catch_all import \
    AddCatchAllRules
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.essence_tiering import \
    AddEssenceTiering
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.hide_unassociated_class_items import \
    HideUnassociatedClassItems
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.item_progressions import \
    AddItemProgressions
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.jewelry_highlights import \
    AddJewelryHighlights
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.league_specific import \
    AddLeagueSpecificDrops
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.misc_currency_tiering import \
    AddMiscCurrenciesTiering
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.orb_tiering import \
    AddOrbTiering
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.show_unassociated_rares import \
    ShowUnassociatedRares
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.skill_gems import \
    AddSkillGems
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.unique_highlights import \
    HighlightUniques
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipes.vendor_recipe_highlights import \
    HighlightVendorRecipes


class FilterConstructionPipeline(AbPipeline):
    def __init__(self, logger: HoornLogger):
        self._pipeline_prefix: str = "FilterConstructionPipeline"

        self._rule_factory: RuleFactory = RuleFactory(logger)
        self._condition_factory: ConditionFactory = ConditionFactory()

        super().__init__(logger, pipeline_descriptor=self._pipeline_prefix)
        self._logger.trace("Successfully initialized.", separator=self._separator)

    def build_pipeline(self):
        self._add_step(AddSkillGems(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[5000] Skill Gems"))
        self._add_step(AddLeagueSpecificDrops(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[6000] League Specific Drops"))
        self._add_step(AddOrbTiering(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[7100] Currencies - Orbs (Campaign)"))
        self._add_step(AddEssenceTiering(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[7200] Currencies - Essences (Campaign)"))
        self._add_step(AddMiscCurrenciesTiering(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[7300] Currencies - Misc (Campaign)"))
        self._add_step(HighlightUniques(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8000] Unique Highlights (Campaign)"))
        self._add_step(HighlightVendorRecipes(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8100] Vendor Recipe Highlights (Campaign)"))
        self._add_step(ShowUnassociatedRares(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8200] Show Unassociated Class-Item Rares (Campaign)"))
        self._add_step(HideUnassociatedClassItems(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8250] Hide Unassociated Class-Items (Campaign)"))
        self._add_step(AddItemProgressions(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8300] Item Progressions (Campaign)"))
        self._add_step(AddJewelryHighlights(self._logger, self._condition_factory, self._rule_factory, self._pipeline_prefix, "[8400] Jewelry Highlights (Campaign)"))
        self._add_step(AddCatchAllRules(self._logger, self._rule_factory, self._pipeline_prefix, "[9999] Catch All"))
