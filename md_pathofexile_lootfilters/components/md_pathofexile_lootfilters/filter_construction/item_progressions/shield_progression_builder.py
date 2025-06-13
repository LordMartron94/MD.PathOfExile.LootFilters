from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import WeaponTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.configs import \
    RarityRuleConfig, ClassRuleConfig, ItemProgressionConfig
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory, get_item_progression_for_category
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_weaponry_and_equipment_styles
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.item_progression_builder import \
    ItemProgressionBuilder


class ShieldProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)


    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        _item_progression: List[ItemProgressionItem] = get_item_progression_for_category(BaseTypeCategory.shields, data.base_type_data)
        normal, magic, rare = determine_weaponry_and_equipment_styles(data)
        item_progression_config: ItemProgressionConfig = ItemProgressionConfig(
            class_rule=ClassRuleConfig(
                show_acts=(Act.Act1, Act.Act1),
                show_rarities={
                    "Normal": normal,
                    "Magic": magic,
                },
                hide_rarities=["Normal", "Magic", "Rare"],
                hide_acts=(Act.Act2, Act.Act10),
            ),
            rarity_rules=[
                RarityRuleConfig("Rare", rare, (Act.Act1, Act.Act10), extra_conditions=[]),
            ]
        )

        return self._builder.build(
            _item_progression,
            WeaponTypeClass.Shields,
            item_progression_config
        )
