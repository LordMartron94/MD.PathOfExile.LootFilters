from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import ArmorTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.configs import \
    ItemProgressionConfig, ClassRuleConfig, RarityRuleConfig
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_weaponry_and_equipment_styles, get_weapon_style_from_tier, get_weaponry_and_equipment_tier


def get_default_item_progression_config(
        data: FilterConstructionPipelineContext,
        rule_factory: RuleFactory,
        condition_factory: ConditionFactory,
        type_class: ArmorTypeClass
) -> ItemProgressionConfig:
    normal, magic, rare = determine_weaponry_and_equipment_styles(data)
    unassociated_rare = get_weapon_style_from_tier(data, get_weaponry_and_equipment_tier("Unassociated_Rare"))
    unassociated_rare_rule = rule_factory.get_rule(RuleType.SHOW, conditions=[
        condition_factory.create_condition(ConditionKeyWord.Class, operator=None, value=f'{type_class.value}'),
        condition_factory.create_condition(ConditionKeyWord.Rarity, operator=ConditionOperator.exact_match, value='"Rare"')
    ] + ConditionGroupFactory.between_acts(condition_factory, Act.Act1, Act.Act10), style=unassociated_rare)

    evasion_condition = condition_factory.create_condition(ConditionKeyWord.BaseEvasion, operator=ConditionOperator.exact_match, value=0)

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
            RarityRuleConfig("Rare", rare, (Act.Act1, Act.Act10), extra_conditions=[evasion_condition])
        ],
        appendix_rules=[unassociated_rare_rule]
    )

    return item_progression_config
