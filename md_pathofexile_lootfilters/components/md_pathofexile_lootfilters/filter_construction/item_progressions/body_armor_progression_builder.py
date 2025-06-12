from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.body_armor_base_type import \
    BodyArmorBaseType
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
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_styles import \
    determine_weaponry_and_equipment_styles


class BodyArmorProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory
        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)

        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=BodyArmorBaseType.PlateVest,           start_level=1,  end_level=1),
            ItemProgressionItem(base_type=BodyArmorBaseType.ShabbyJerkin,        start_level=2,  end_level=2),
            ItemProgressionItem(base_type=BodyArmorBaseType.SimpleRobe,          start_level=3,  end_level=3),
            ItemProgressionItem(base_type=BodyArmorBaseType.ScaleVest,           start_level=3,  end_level=4),
            ItemProgressionItem(base_type=BodyArmorBaseType.ChainmailVest,       start_level=3,  end_level=4),
            ItemProgressionItem(base_type=BodyArmorBaseType.PaddedVest,          start_level=4,  end_level=5),
            ItemProgressionItem(base_type=BodyArmorBaseType.Chestplate,          start_level=6,  end_level=7),
            ItemProgressionItem(base_type=BodyArmorBaseType.LightBrigandine,     start_level=7,  end_level=8),
            ItemProgressionItem(base_type=BodyArmorBaseType.ChainmailTunic,      start_level=8,  end_level=8),
            ItemProgressionItem(base_type=BodyArmorBaseType.StrappedLeather,     start_level=8,  end_level=9),
            ItemProgressionItem(base_type=BodyArmorBaseType.OiledVest,           start_level=9,  end_level=10),
            ItemProgressionItem(base_type=BodyArmorBaseType.SilkenVest,          start_level=11, end_level=16),
            ItemProgressionItem(base_type=BodyArmorBaseType.CopperPlate,         start_level=16, end_level=17),
            ItemProgressionItem(base_type=BodyArmorBaseType.BuckskinTunic,       start_level=16, end_level=17),
            ItemProgressionItem(base_type=BodyArmorBaseType.ScaleDoublet,        start_level=16, end_level=17),
            ItemProgressionItem(base_type=BodyArmorBaseType.RingmailCoat,        start_level=17, end_level=17),
            ItemProgressionItem(base_type=BodyArmorBaseType.ScholarsRobe,        start_level=17, end_level=18),
            ItemProgressionItem(base_type=BodyArmorBaseType.PaddedJacket,        start_level=18, end_level=20),
            ItemProgressionItem(base_type=BodyArmorBaseType.WarPlate,            start_level=20, end_level=21),
            ItemProgressionItem(base_type=BodyArmorBaseType.InfantryBrigandine,  start_level=20, end_level=21),
            ItemProgressionItem(base_type=BodyArmorBaseType.ChainmailDoublet,     start_level=21, end_level=21),
            ItemProgressionItem(base_type=BodyArmorBaseType.OiledCoat,           start_level=22, end_level=24),
            ItemProgressionItem(base_type=BodyArmorBaseType.WildLeather,         start_level=24, end_level=25),
            ItemProgressionItem(base_type=BodyArmorBaseType.SilkenGarb,          start_level=25, end_level=27),

            ItemProgressionItem(base_type=BodyArmorBaseType.FullPlate,           start_level=27, end_level=28),
            ItemProgressionItem(base_type=BodyArmorBaseType.FullLeather,         start_level=27, end_level=28),
            ItemProgressionItem(base_type=BodyArmorBaseType.MagesVestment,       start_level=27, end_level=28),
            ItemProgressionItem(base_type=BodyArmorBaseType.FullScaleArmour,     start_level=27, end_level=28),
            ItemProgressionItem(base_type=BodyArmorBaseType.FullRingmail,        start_level=27, end_level=28),
            ItemProgressionItem(base_type=BodyArmorBaseType.ScarletRaiment,      start_level=28, end_level=31),
            ItemProgressionItem(base_type=BodyArmorBaseType.ArenaPlate,          start_level=31, end_level=32),
            ItemProgressionItem(base_type=BodyArmorBaseType.SunLeather,          start_level=31, end_level=32),
            ItemProgressionItem(base_type=BodyArmorBaseType.SilkRobe,            start_level=31, end_level=32),
            ItemProgressionItem(base_type=BodyArmorBaseType.SoldiersBrigandine,  start_level=31, end_level=32),
            ItemProgressionItem(base_type=BodyArmorBaseType.FullChainmail,       start_level=31, end_level=32),
            ItemProgressionItem(base_type=BodyArmorBaseType.WaxedGarb,           start_level=32, end_level=34),
            ItemProgressionItem(base_type=BodyArmorBaseType.LordlyPlate,         start_level=34, end_level=35),
            ItemProgressionItem(base_type=BodyArmorBaseType.ThiefsGarb,          start_level=34, end_level=35),
            ItemProgressionItem(base_type=BodyArmorBaseType.CabalistRegalia,     start_level=34, end_level=35),
            ItemProgressionItem(base_type=BodyArmorBaseType.FieldLamellar,       start_level=34, end_level=35),
            ItemProgressionItem(base_type=BodyArmorBaseType.HolyChainmail,       start_level=34, end_level=35),
            ItemProgressionItem(base_type=BodyArmorBaseType.BoneArmour,          start_level=35, end_level=36),
            ItemProgressionItem(base_type=BodyArmorBaseType.BronzePlate,         start_level=36, end_level=37),
            ItemProgressionItem(base_type=BodyArmorBaseType.EelskinTunic,        start_level=36, end_level=37),
            ItemProgressionItem(base_type=BodyArmorBaseType.SagesRobe,           start_level=37, end_level=37),
            ItemProgressionItem(base_type=BodyArmorBaseType.WyrmscaleDoublet,    start_level=38, end_level=38),
            ItemProgressionItem(base_type=BodyArmorBaseType.LatticedRingmail,    start_level=39, end_level=39),
            ItemProgressionItem(base_type=BodyArmorBaseType.QuiltedJacket,       start_level=40, end_level=40),
            ItemProgressionItem(base_type=BodyArmorBaseType.BattlePlate,         start_level=40, end_level=41),

            ItemProgressionItem(base_type=BodyArmorBaseType.FrontierLeather,     start_level=40, end_level=41),
            ItemProgressionItem(base_type=BodyArmorBaseType.SilkenWrap,          start_level=41, end_level=41),
            ItemProgressionItem(base_type=BodyArmorBaseType.HussarBrigandine,    start_level=42, end_level=42),
            ItemProgressionItem(base_type=BodyArmorBaseType.CrusaderChainmail,   start_level=43, end_level=43),
            ItemProgressionItem(base_type=BodyArmorBaseType.SleekCoat,           start_level=44, end_level=44),
            ItemProgressionItem(base_type=BodyArmorBaseType.SunPlate,            start_level=44, end_level=45),
            ItemProgressionItem(base_type=BodyArmorBaseType.GloriousLeather,     start_level=44, end_level=45),
            ItemProgressionItem(base_type=BodyArmorBaseType.ConjurersVestment,   start_level=45, end_level=45),
            ItemProgressionItem(base_type=BodyArmorBaseType.FullWyrmscale,       start_level=46, end_level=46),
            ItemProgressionItem(base_type=BodyArmorBaseType.OrnateRingmail,      start_level=47, end_level=47),
            ItemProgressionItem(base_type=BodyArmorBaseType.CrimsonRaiment,      start_level=48, end_level=48),
            ItemProgressionItem(base_type=BodyArmorBaseType.ColosseumPlate,      start_level=48, end_level=49),
            ItemProgressionItem(base_type=BodyArmorBaseType.CoronalLeather,      start_level=48, end_level=49),
            ItemProgressionItem(base_type=BodyArmorBaseType.SpidersilkRobe,      start_level=49, end_level=49),
            ItemProgressionItem(base_type=BodyArmorBaseType.CommandersBrigandine, start_level=50, end_level=50),
            ItemProgressionItem(base_type=BodyArmorBaseType.ChainHauberk,        start_level=51, end_level=51),
            ItemProgressionItem(base_type=BodyArmorBaseType.LacqueredGarb,       start_level=52, end_level=52),
            ItemProgressionItem(base_type=BodyArmorBaseType.MajesticPlate,       start_level=52, end_level=53),
            ItemProgressionItem(base_type=BodyArmorBaseType.CutthroatsGarb,      start_level=52, end_level=53),
            ItemProgressionItem(base_type=BodyArmorBaseType.DestroyerRegalia,    start_level=53, end_level=53),
            ItemProgressionItem(base_type=BodyArmorBaseType.BattleLamellar,      start_level=54, end_level=54),
            ItemProgressionItem(base_type=BodyArmorBaseType.DevoutChainmail,     start_level=55, end_level=55),
            ItemProgressionItem(base_type=BodyArmorBaseType.GoldenPlate,         start_level=55, end_level=56),
            ItemProgressionItem(base_type=BodyArmorBaseType.SharkskinTunic,      start_level=55, end_level=56),
            ItemProgressionItem(base_type=BodyArmorBaseType.SavantsRobe,         start_level=55, end_level=56),

            ItemProgressionItem(base_type=BodyArmorBaseType.CryptArmour,         start_level=56, end_level=56),
            ItemProgressionItem(base_type=BodyArmorBaseType.DragonscaleDoublet,  start_level=57, end_level=57),
            ItemProgressionItem(base_type=BodyArmorBaseType.LoricatedRingmail,   start_level=58, end_level=58),
            ItemProgressionItem(base_type=BodyArmorBaseType.CrusaderPlate,       start_level=58, end_level=59),
            ItemProgressionItem(base_type=BodyArmorBaseType.DestinyLeather,      start_level=58, end_level=59),
            ItemProgressionItem(base_type=BodyArmorBaseType.NecromancerSilks,    start_level=58, end_level=59),
            ItemProgressionItem(base_type=BodyArmorBaseType.SentinelJacket,      start_level=59, end_level=59),
            ItemProgressionItem(base_type=BodyArmorBaseType.DesertBrigandine,    start_level=60, end_level=60),
            ItemProgressionItem(base_type=BodyArmorBaseType.ConquestChainmail,   start_level=61, end_level=61),
            ItemProgressionItem(base_type=BodyArmorBaseType.AstralPlate,         start_level=61, end_level=62),
            ItemProgressionItem(base_type=BodyArmorBaseType.ExquisiteLeather,    start_level=61, end_level=62),
            ItemProgressionItem(base_type=BodyArmorBaseType.OccultistsVestment,  start_level=61, end_level=62),
            ItemProgressionItem(base_type=BodyArmorBaseType.VarnishedCoat,       start_level=62, end_level=62),
            ItemProgressionItem(base_type=BodyArmorBaseType.FullDragonscale,     start_level=63, end_level=63),
            ItemProgressionItem(base_type=BodyArmorBaseType.ElegantRingmail,     start_level=64, end_level=65),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        normal, magic, rare = determine_weaponry_and_equipment_styles(data)

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
            ArmorTypeClass.BodyArmor,
            item_progression_config
        )
