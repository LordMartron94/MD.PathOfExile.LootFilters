from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.belt_base_type import BeltBaseType
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
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_weapon_tier_style import \
    determine_styles


class BeltProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)

        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=BeltBaseType.ChainBelt,   start_level=1,  end_level=2),
            ItemProgressionItem(base_type=BeltBaseType.RusticSash,  start_level=2,  end_level=9),
            ItemProgressionItem(base_type=BeltBaseType.HeavyBelt,   start_level=9,  end_level=10),
            ItemProgressionItem(base_type=BeltBaseType.LeatherBelt, start_level=10, end_level=19),
            ItemProgressionItem(base_type=BeltBaseType.ClothBelt,   start_level=19, end_level=20),
            ItemProgressionItem(base_type=BeltBaseType.StuddedBelt, start_level=20, end_level=65),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        normal, magic, rare = determine_styles(data)
        return self._builder.build(
            self._item_progression,
            ArmorTypeClass.Belts,
            {"Normal": normal, "Magic": magic, "Rare": rare},
        )
