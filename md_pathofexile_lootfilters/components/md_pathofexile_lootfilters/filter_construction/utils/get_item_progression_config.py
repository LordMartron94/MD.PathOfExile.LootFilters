from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.configs import \
    ItemProgressionConfig, ClassRuleConfig, RarityRuleConfig
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_weaponry_and_equipment_styles, get_weapon_style_from_tier, get_weaponry_and_equipment_tier


def get_default_item_progression_config(
        data: FilterConstructionPipelineContext,
        condition_factory: ConditionFactory
) -> ItemProgressionConfig:
    normal, magic, rare = determine_weaponry_and_equipment_styles(data)

    extra_conditions = [
        condition_factory.create_condition(ConditionKeyWord.BaseEvasion, operator=ConditionOperator.exact_match, value=0)
    ]

    item_progression_config: ItemProgressionConfig = ItemProgressionConfig(
        class_rule=ClassRuleConfig(
            show_acts=(Act.Act1, Act.Act1),
            show_rarities={
                "Normal": normal,
                "Magic": magic,
            },
            hide_rarities=["Normal", "Magic"],
            hide_acts=(Act.Act1, Act.Act10),
        ),
        rarity_rules=[
            RarityRuleConfig("Rare", rare, (Act.Act1, Act.Act10), extra_conditions=extra_conditions),
            RarityRuleConfig("Rare", get_weapon_style_from_tier(data, get_weaponry_and_equipment_tier("Unassociated_Rare")), (Act.Act1, Act.Act10), extra_conditions=[]),
        ]
    )

    return item_progression_config
