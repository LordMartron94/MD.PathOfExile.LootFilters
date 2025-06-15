from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import ArmorTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.item_progression_builder import \
    ItemProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory, get_item_progression_for_category
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_item_progression_config import \
    get_default_item_progression_config


class GloveProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._rule_factory = rule_factory

        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        _item_progression: List[ItemProgressionItem] = get_item_progression_for_category(BaseTypeCategory.gloves, data.base_type_data)
        item_progression_config = get_default_item_progression_config(data, self._rule_factory, self._condition_factory, ArmorTypeClass.Gloves)

        return self._builder.build(
            _item_progression,
            ArmorTypeClass.Gloves,
            item_progression_config
        )
