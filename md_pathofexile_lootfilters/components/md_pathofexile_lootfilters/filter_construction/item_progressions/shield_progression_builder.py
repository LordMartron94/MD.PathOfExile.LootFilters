from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.shield_base_type import ShieldBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.block_factory import RuleFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_factory import \
    ConditionFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import WeaponTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.get_weapon_tier_style import \
    determine_styles
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_progressions.item_progression_builder import \
    ItemProgressionBuilder


class ShieldProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)

        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=ShieldBaseType.SplinteredTowerShield,    start_level=1,  end_level=1),
            ItemProgressionItem(base_type=ShieldBaseType.GoathideBuckler,          start_level=2,  end_level=2),
            ItemProgressionItem(base_type=ShieldBaseType.TwigSpiritShield,         start_level=3,  end_level=4),
            ItemProgressionItem(base_type=ShieldBaseType.CorrodedTowerShield,      start_level=5,  end_level=6),
            ItemProgressionItem(base_type=ShieldBaseType.RottedRoundShield,        start_level=5,  end_level=6),
            ItemProgressionItem(base_type=ShieldBaseType.SpikedBundle,             start_level=5,  end_level=6),
            ItemProgressionItem(base_type=ShieldBaseType.PlankKiteShield,          start_level=7,  end_level=7),
            ItemProgressionItem(base_type=ShieldBaseType.PineBuckler,              start_level=8,  end_level=8),
            ItemProgressionItem(base_type=ShieldBaseType.YewSpiritShield,          start_level=9,  end_level=10),
            ItemProgressionItem(base_type=ShieldBaseType.RawhideTowerShield,       start_level=11, end_level=11),
            ItemProgressionItem(base_type=ShieldBaseType.FirRoundShield,           start_level=12, end_level=12),
            ItemProgressionItem(base_type=ShieldBaseType.DriftwoodSpikedShield,    start_level=12, end_level=12),
            ItemProgressionItem(base_type=ShieldBaseType.LindenKiteShield,         start_level=13, end_level=14),
            ItemProgressionItem(base_type=ShieldBaseType.BoneSpiritShield,         start_level=15, end_level=15),
            ItemProgressionItem(base_type=ShieldBaseType.PaintedBuckler,           start_level=16, end_level=16),
            ItemProgressionItem(base_type=ShieldBaseType.CedarTowerShield,         start_level=17, end_level=19),
            ItemProgressionItem(base_type=ShieldBaseType.StuddedRoundShield,       start_level=20, end_level=20),
            ItemProgressionItem(base_type=ShieldBaseType.ReinforcedKiteShield,     start_level=20, end_level=20),
            ItemProgressionItem(base_type=ShieldBaseType.AlloyedSpikedShield,      start_level=20, end_level=22),
            ItemProgressionItem(base_type=ShieldBaseType.HammeredBuckler,          start_level=23, end_level=23),
            ItemProgressionItem(base_type=ShieldBaseType.TarnishedSpiritShield,    start_level=23, end_level=23),
            ItemProgressionItem(base_type=ShieldBaseType.CopperTowerShield,        start_level=24, end_level=26),
            ItemProgressionItem(base_type=ShieldBaseType.ScarletRoundShield,       start_level=27, end_level=27),
            ItemProgressionItem(base_type=ShieldBaseType.LayeredKiteShield,        start_level=27, end_level=27),
            ItemProgressionItem(base_type=ShieldBaseType.BurnishedSpikedShield,    start_level=27, end_level=27),
            ItemProgressionItem(base_type=ShieldBaseType.JinglingSpiritShield,     start_level=28, end_level=28),
            ItemProgressionItem(base_type=ShieldBaseType.WarBuckler,               start_level=29, end_level=29),
            ItemProgressionItem(base_type=ShieldBaseType.ReinforcedTowerShield,    start_level=30, end_level=32),
            ItemProgressionItem(base_type=ShieldBaseType.BrassSpiritShield,        start_level=33, end_level=33),
            ItemProgressionItem(base_type=ShieldBaseType.SplendidRoundShield,      start_level=33, end_level=33),
            ItemProgressionItem(base_type=ShieldBaseType.OrnateSpikedShield,       start_level=33, end_level=33),
            ItemProgressionItem(base_type=ShieldBaseType.GildedBuckler,            start_level=34, end_level=34),
            ItemProgressionItem(base_type=ShieldBaseType.CeremonialKiteShield,     start_level=34, end_level=34),
            ItemProgressionItem(base_type=ShieldBaseType.PaintedTowerShield,       start_level=35, end_level=36),
            ItemProgressionItem(base_type=ShieldBaseType.WalnutSpiritShield,       start_level=37, end_level=37),
            ItemProgressionItem(base_type=ShieldBaseType.OakBuckler,               start_level=38, end_level=38),
            ItemProgressionItem(base_type=ShieldBaseType.BuckskinTowerShield,      start_level=39, end_level=39),
            ItemProgressionItem(base_type=ShieldBaseType.MapleRoundShield,         start_level=39, end_level=39),
            ItemProgressionItem(base_type=ShieldBaseType.RedwoodSpikedShield,      start_level=39, end_level=39),
            ItemProgressionItem(base_type=ShieldBaseType.EtchedKiteShield,         start_level=40, end_level=40),
            ItemProgressionItem(base_type=ShieldBaseType.IvorySpiritShield,        start_level=41, end_level=41),
            ItemProgressionItem(base_type=ShieldBaseType.EnameledBuckler,          start_level=42, end_level=42),
            ItemProgressionItem(base_type=ShieldBaseType.MahoganyTowerShield,      start_level=43, end_level=44),
            ItemProgressionItem(base_type=ShieldBaseType.AncientSpiritShield,      start_level=45, end_level=45),
            ItemProgressionItem(base_type=ShieldBaseType.SpikedRoundShield,        start_level=45, end_level=45),
            ItemProgressionItem(base_type=ShieldBaseType.CompoundSpikedShield,     start_level=45, end_level=45),
            ItemProgressionItem(base_type=ShieldBaseType.CorrugatedBuckler,        start_level=46, end_level=46),
            ItemProgressionItem(base_type=ShieldBaseType.SteelKiteShield,          start_level=46, end_level=46),
            ItemProgressionItem(base_type=ShieldBaseType.BronzeTowerShield,        start_level=47, end_level=48),
            ItemProgressionItem(base_type=ShieldBaseType.ChimingSpiritShield,      start_level=49, end_level=49),
            ItemProgressionItem(base_type=ShieldBaseType.CrimsonRoundShield,       start_level=49, end_level=49),
            ItemProgressionItem(base_type=ShieldBaseType.PolishedSpikedShield,     start_level=49, end_level=49),
            ItemProgressionItem(base_type=ShieldBaseType.BattleBuckler,            start_level=50, end_level=50),
            ItemProgressionItem(base_type=ShieldBaseType.LaminatedKiteShield,      start_level=50, end_level=50),
            ItemProgressionItem(base_type=ShieldBaseType.GirdedTowerShield,        start_level=51, end_level=52),
            ItemProgressionItem(base_type=ShieldBaseType.ThoriumSpiritShield,      start_level=53, end_level=53),
            ItemProgressionItem(base_type=ShieldBaseType.GoldenBuckler,            start_level=54, end_level=54),
            ItemProgressionItem(base_type=ShieldBaseType.BaroqueRoundShield,       start_level=54, end_level=54),
            ItemProgressionItem(base_type=ShieldBaseType.SovereignSpikedShield,    start_level=54, end_level=54),
            ItemProgressionItem(base_type=ShieldBaseType.CrestedTowerShield,       start_level=55, end_level=55),
            ItemProgressionItem(base_type=ShieldBaseType.AngelicKiteShield,        start_level=55, end_level=55),
            ItemProgressionItem(base_type=ShieldBaseType.LacewoodSpiritShield,     start_level=56, end_level=56),
            ItemProgressionItem(base_type=ShieldBaseType.IronwoodBuckler,          start_level=57, end_level=57),
            ItemProgressionItem(base_type=ShieldBaseType.ShagreenTowerShield,      start_level=58, end_level=58),
            ItemProgressionItem(base_type=ShieldBaseType.TeakRoundShield,          start_level=58, end_level=58),
            ItemProgressionItem(base_type=ShieldBaseType.AlderSpikedShield,        start_level=58, end_level=58),
            ItemProgressionItem(base_type=ShieldBaseType.FossilisedSpiritShield,   start_level=59, end_level=59),
            ItemProgressionItem(base_type=ShieldBaseType.BrandedKiteShield,        start_level=59, end_level=59),
            ItemProgressionItem(base_type=ShieldBaseType.LacqueredBuckler,         start_level=60, end_level=60),
            ItemProgressionItem(base_type=ShieldBaseType.EbonyTowerShield,         start_level=61, end_level=61),
            ItemProgressionItem(base_type=ShieldBaseType.VaalSpiritShield,         start_level=62, end_level=62),
            ItemProgressionItem(base_type=ShieldBaseType.SpinyRoundShield,         start_level=62, end_level=62),
            ItemProgressionItem(base_type=ShieldBaseType.ChampionKiteShield,       start_level=62, end_level=62),
            ItemProgressionItem(base_type=ShieldBaseType.EzomyteSpikedShield,      start_level=62, end_level=62),
            ItemProgressionItem(base_type=ShieldBaseType.VaalBuckler,              start_level=63, end_level=63),
            ItemProgressionItem(base_type=ShieldBaseType.EzomyteTowerShield,       start_level=64, end_level=65),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        normal, magic, rare = determine_styles(data)
        rules = self._builder.build(self._item_progression, WeaponTypeClass.Shields, {
            "Normal": normal,
            "Magic": magic,
            "Rare": rare,
        })
        return rules
