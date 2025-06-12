from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.helmet_base_type import HelmetBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord, \
    ConditionOperator
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


class HelmetProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)

        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=HelmetBaseType.IronHat,           start_level=1,  end_level=2),
            ItemProgressionItem(base_type=HelmetBaseType.LeatherCap,        start_level=2,  end_level=3),
            ItemProgressionItem(base_type=HelmetBaseType.VineCirclet,       start_level=3,  end_level=3),
            ItemProgressionItem(base_type=HelmetBaseType.BatteredHelm,      start_level=3,  end_level=4),
            ItemProgressionItem(base_type=HelmetBaseType.ScareMask,         start_level=4,  end_level=4),
            ItemProgressionItem(base_type=HelmetBaseType.RustedCoif,        start_level=5,  end_level=6),
            ItemProgressionItem(base_type=HelmetBaseType.ConeHelmet,        start_level=7,  end_level=7),
            ItemProgressionItem(base_type=HelmetBaseType.IronCirclet,       start_level=8,  end_level=9),
            ItemProgressionItem(base_type=HelmetBaseType.Tricorne,          start_level=9,  end_level=10),
            ItemProgressionItem(base_type=HelmetBaseType.PlagueMask, start_level=10, end_level=11),
            ItemProgressionItem(base_type=HelmetBaseType.SoldierHelmet,     start_level=12, end_level=12),
            ItemProgressionItem(base_type=HelmetBaseType.Sallet,            start_level=13, end_level=16),
            ItemProgressionItem(base_type=HelmetBaseType.TortureCage,       start_level=16, end_level=17),
            ItemProgressionItem(base_type=HelmetBaseType.IronMask,          start_level=17, end_level=17),
            ItemProgressionItem(base_type=HelmetBaseType.BarbuteHelmet,     start_level=18, end_level=19),
            ItemProgressionItem(base_type=HelmetBaseType.LeatherHood,       start_level=20, end_level=21),
            ItemProgressionItem(base_type=HelmetBaseType.GreatHelmet,       start_level=22, end_level=22),
            ItemProgressionItem(base_type=HelmetBaseType.VisoredSallet,     start_level=23, end_level=25),
            ItemProgressionItem(base_type=HelmetBaseType.CloseHelmet,       start_level=25, end_level=26),
            ItemProgressionItem(base_type=HelmetBaseType.TribalCirclet,     start_level=26, end_level=27),
            ItemProgressionItem(base_type=HelmetBaseType.FestivalMask,      start_level=28, end_level=29),
            ItemProgressionItem(base_type=HelmetBaseType.WolfPelt,          start_level=30, end_level=30),
            ItemProgressionItem(base_type=HelmetBaseType.CrusaderHelmet,    start_level=31, end_level=32),
            ItemProgressionItem(base_type=HelmetBaseType.GildedSallet,      start_level=33, end_level=33),

            ItemProgressionItem(base_type=HelmetBaseType.BoneCirclet,       start_level=34, end_level=34),
            ItemProgressionItem(base_type=HelmetBaseType.GladiatorHelmet,   start_level=34, end_level=35),
            ItemProgressionItem(base_type=HelmetBaseType.GoldenMask,        start_level=35, end_level=35),
            ItemProgressionItem(base_type=HelmetBaseType.SecutorHelm,       start_level=36, end_level=36),
            ItemProgressionItem(base_type=HelmetBaseType.AventailHelmet,    start_level=37, end_level=37),
            ItemProgressionItem(base_type=HelmetBaseType.RavenMask,         start_level=38, end_level=38),
            ItemProgressionItem(base_type=HelmetBaseType.LunarisCirclet,    start_level=39, end_level=39),
            ItemProgressionItem(base_type=HelmetBaseType.ReaverHelmet,      start_level=40, end_level=40),
            ItemProgressionItem(base_type=HelmetBaseType.HunterHood,        start_level=41, end_level=42),
            ItemProgressionItem(base_type=HelmetBaseType.FencerHelm,        start_level=43, end_level=43),
            ItemProgressionItem(base_type=HelmetBaseType.ZealotHelmet,      start_level=44, end_level=44),
            ItemProgressionItem(base_type=HelmetBaseType.CallousMask,       start_level=45, end_level=46),
            ItemProgressionItem(base_type=HelmetBaseType.NobleTricorne,     start_level=47, end_level=47),
            ItemProgressionItem(base_type=HelmetBaseType.SiegeHelmet,       start_level=47, end_level=48),
            ItemProgressionItem(base_type=HelmetBaseType.SteelCirclet,      start_level=48, end_level=50),
            ItemProgressionItem(base_type=HelmetBaseType.LacqueredHelmet,   start_level=51, end_level=51),
            ItemProgressionItem(base_type=HelmetBaseType.RegicideMask,      start_level=52, end_level=52),
            ItemProgressionItem(base_type=HelmetBaseType.GreatCrown,        start_level=53, end_level=53),
            ItemProgressionItem(base_type=HelmetBaseType.NecromancerCirclet, start_level=54, end_level=54),
            ItemProgressionItem(base_type=HelmetBaseType.SamniteHelmet,     start_level=54, end_level=55),
            ItemProgressionItem(base_type=HelmetBaseType.UrsinePelt,        start_level=55, end_level=56),
            ItemProgressionItem(base_type=HelmetBaseType.HarlequinMask,     start_level=57, end_level=57),
            ItemProgressionItem(base_type=HelmetBaseType.FlutedBascinet,    start_level=57, end_level=58),
            ItemProgressionItem(base_type=HelmetBaseType.MagistrateCrown,   start_level=58, end_level=58),
            ItemProgressionItem(base_type=HelmetBaseType.SolarisCirclet,    start_level=59, end_level=59),

            ItemProgressionItem(base_type=HelmetBaseType.EzomyteBurgonet,   start_level=59, end_level=60),
            ItemProgressionItem(base_type=HelmetBaseType.SilkenHood,        start_level=60, end_level=61),
            ItemProgressionItem(base_type=HelmetBaseType.VaalMask,          start_level=62, end_level=62),
            ItemProgressionItem(base_type=HelmetBaseType.PigFacedBascinet,  start_level=62, end_level=63),
            ItemProgressionItem(base_type=HelmetBaseType.ProphetCrown,      start_level=63, end_level=63),
            ItemProgressionItem(base_type=HelmetBaseType.SinnerTricorne,    start_level=64, end_level=65),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        normal, magic, rare = determine_styles(data)

        extra_conditions = [
            self._condition_factory.create_condition(ConditionKeyWord.BaseEvasion, operator=ConditionOperator.exact_match, value=0)
        ]

        return self._builder.build(
            self._item_progression,
            ArmorTypeClass.Helmets,
            {"Normal": normal, "Magic": magic, "Rare": rare},
            rarity_extra_conditions={
                "Normal": extra_conditions,
                "Magic": extra_conditions,
                "Rare": extra_conditions
            }
        )
