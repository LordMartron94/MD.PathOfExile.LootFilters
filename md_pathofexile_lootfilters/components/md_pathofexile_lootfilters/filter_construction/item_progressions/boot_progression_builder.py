from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.boot_base_type import BootBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import ArmorTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.item_progression_builder import \
    ItemProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.configs import \
    ItemProgressionConfig, ClassRuleConfig, RarityRuleConfig
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_weapon_tier_style import \
    determine_styles


class BootProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)

        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=BootBaseType.IronGreaves,       start_level=1,  end_level=2),
            ItemProgressionItem(base_type=BootBaseType.RawhideBoots,      start_level=2,  end_level=3),
            ItemProgressionItem(base_type=BootBaseType.WoolShoes,         start_level=3,  end_level=4),
            ItemProgressionItem(base_type=BootBaseType.ChainBoots,        start_level=5,  end_level=5),
            ItemProgressionItem(base_type=BootBaseType.LeatherscaleBoots, start_level=5,  end_level=6),
            ItemProgressionItem(base_type=BootBaseType.WrappedBoots,      start_level=6,  end_level=8),
            ItemProgressionItem(base_type=BootBaseType.SteelGreaves,      start_level=8,  end_level=9),
            ItemProgressionItem(base_type=BootBaseType.VelvetSlippers,    start_level=9,  end_level=11),
            ItemProgressionItem(base_type=BootBaseType.GoathideBoots,     start_level=12, end_level=12),
            ItemProgressionItem(base_type=BootBaseType.RingmailBoots,     start_level=13, end_level=15),
            ItemProgressionItem(base_type=BootBaseType.StrappedBoots,     start_level=16, end_level=17),
            ItemProgressionItem(base_type=BootBaseType.IronscaleBoots,    start_level=18, end_level=21),
            ItemProgressionItem(base_type=BootBaseType.DeerskinBoots,     start_level=21, end_level=22),
            ItemProgressionItem(base_type=BootBaseType.SilkSlippers,      start_level=22, end_level=22),
            ItemProgressionItem(base_type=BootBaseType.PlatedGreaves,     start_level=23, end_level=26),
            ItemProgressionItem(base_type=BootBaseType.ClaspedBoots,      start_level=27, end_level=27),
            ItemProgressionItem(base_type=BootBaseType.MeshBoots,         start_level=28, end_level=29),
            ItemProgressionItem(base_type=BootBaseType.BronzescaleBoots,  start_level=30, end_level=31),
            ItemProgressionItem(base_type=BootBaseType.ScholarBoots,      start_level=32, end_level=32),
            ItemProgressionItem(base_type=BootBaseType.ReinforcedGreaves, start_level=33, end_level=33),
            ItemProgressionItem(base_type=BootBaseType.NubuckBoots,       start_level=33, end_level=34),
            ItemProgressionItem(base_type=BootBaseType.ShackledBoots,     start_level=34, end_level=35),
            ItemProgressionItem(base_type=BootBaseType.SteelscaleBoots,   start_level=35, end_level=36),
            ItemProgressionItem(base_type=BootBaseType.RivetedBoots,      start_level=36, end_level=36),
            ItemProgressionItem(base_type=BootBaseType.AntiqueGreaves,    start_level=37, end_level=37),
            ItemProgressionItem(base_type=BootBaseType.SatinSlippers,     start_level=38, end_level=38),
            ItemProgressionItem(base_type=BootBaseType.EelskinBoots,      start_level=39, end_level=39),
            ItemProgressionItem(base_type=BootBaseType.ZealotBoots,       start_level=40, end_level=40),
            ItemProgressionItem(base_type=BootBaseType.TrapperBoots,      start_level=41, end_level=41),
            ItemProgressionItem(base_type=BootBaseType.SerpentscaleBoots, start_level=42, end_level=43),
            ItemProgressionItem(base_type=BootBaseType.SharkskinBoots,    start_level=43, end_level=44),
            ItemProgressionItem(base_type=BootBaseType.SamiteSlippers,    start_level=44, end_level=45),
            ItemProgressionItem(base_type=BootBaseType.AncientGreaves,    start_level=46, end_level=46),
            ItemProgressionItem(base_type=BootBaseType.AmbushBoots,       start_level=47, end_level=48),
            ItemProgressionItem(base_type=BootBaseType.SoldierBoots,      start_level=49, end_level=50),
            ItemProgressionItem(base_type=BootBaseType.WyrmscaleBoots,    start_level=51, end_level=52),
            ItemProgressionItem(base_type=BootBaseType.ConjurerBoots,     start_level=53, end_level=53),
            ItemProgressionItem(base_type=BootBaseType.GoliathGreaves,    start_level=54, end_level=54),
            ItemProgressionItem(base_type=BootBaseType.ShagreenBoots,     start_level=54, end_level=55),
            ItemProgressionItem(base_type=BootBaseType.CarnalBoots,       start_level=55, end_level=57),
            ItemProgressionItem(base_type=BootBaseType.LegionBoots,       start_level=58, end_level=58),
            ItemProgressionItem(base_type=BootBaseType.HydrascaleBoots,   start_level=59, end_level=60),
            ItemProgressionItem(base_type=BootBaseType.ArcanistSlippers,  start_level=61, end_level=61),
            ItemProgressionItem(base_type=BootBaseType.VaalGreaves,       start_level=61, end_level=62),
            ItemProgressionItem(base_type=BootBaseType.StealthBoots,      start_level=62, end_level=62),
            ItemProgressionItem(base_type=BootBaseType.AssassinsBoots,    start_level=63, end_level=63),
            ItemProgressionItem(base_type=BootBaseType.CrusaderBoots,     start_level=64, end_level=65),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        normal, magic, rare = determine_styles(data)

        extra_conditions = [
            self._condition_factory.create_condition(ConditionKeyWord.BaseEvasion, operator=ConditionOperator.exact_match, value=0)
        ]

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
                RarityRuleConfig("Rare", rare, (Act.Act1, Act.Act10), extra_conditions=extra_conditions),
            ]
        )

        return self._builder.build(
            self._item_progression,
            ArmorTypeClass.Boots,
            item_progression_config
        )
