from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.glove_base_type import GloveBaseType
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


class GloveProgressionBuilder:
    def __init__(self, condition_factory: ConditionFactory, rule_factory: RuleFactory):
        self._condition_factory = condition_factory

        self._builder = ItemProgressionBuilder(condition_factory, rule_factory)
        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=GloveBaseType.IronGauntlets,        start_level=1,  end_level=2),
            ItemProgressionItem(base_type=GloveBaseType.RawhideGloves,        start_level=2,  end_level=3),
            ItemProgressionItem(base_type=GloveBaseType.WoolGloves,           start_level=3,  end_level=3),
            ItemProgressionItem(base_type=GloveBaseType.FishscaleGauntlets,   start_level=4,  end_level=4),
            ItemProgressionItem(base_type=GloveBaseType.WrappedMitts,         start_level=5,  end_level=6),
            ItemProgressionItem(base_type=GloveBaseType.ChainGloves,          start_level=7,  end_level=8),
            ItemProgressionItem(base_type=GloveBaseType.GoathideGloves,       start_level=9,  end_level=10),
            ItemProgressionItem(base_type=GloveBaseType.PlatedGauntlets,      start_level=11, end_level=11),
            ItemProgressionItem(base_type=GloveBaseType.VelvetGloves,         start_level=12, end_level=14),
            ItemProgressionItem(base_type=GloveBaseType.IronscaleGauntlets,   start_level=15, end_level=15),
            ItemProgressionItem(base_type=GloveBaseType.StrappedMitts,        start_level=16, end_level=18),
            ItemProgressionItem(base_type=GloveBaseType.RingmailGloves,       start_level=19, end_level=20),
            ItemProgressionItem(base_type=GloveBaseType.DeerskinGloves,       start_level=21, end_level=22),
            ItemProgressionItem(base_type=GloveBaseType.BronzeGauntlets,      start_level=23, end_level=24),
            ItemProgressionItem(base_type=GloveBaseType.SilkGloves,           start_level=25, end_level=26),
            ItemProgressionItem(base_type=GloveBaseType.BronzescaleGauntlets, start_level=27, end_level=30),
            ItemProgressionItem(base_type=GloveBaseType.ClaspedMitts,         start_level=31, end_level=31),
            ItemProgressionItem(base_type=GloveBaseType.MeshGloves,           start_level=32, end_level=32),
            ItemProgressionItem(base_type=GloveBaseType.NubuckGloves,         start_level=33, end_level=34),
            ItemProgressionItem(base_type=GloveBaseType.SteelGauntlets,       start_level=35, end_level=35),
            ItemProgressionItem(base_type=GloveBaseType.EmbroideredGloves,    start_level=35, end_level=36),
            ItemProgressionItem(base_type=GloveBaseType.SteelscaleGauntlets,  start_level=35, end_level=36),
            ItemProgressionItem(base_type=GloveBaseType.TrapperMitts,         start_level=36, end_level=36),
            ItemProgressionItem(base_type=GloveBaseType.RivetedGloves,        start_level=37, end_level=37),
            ItemProgressionItem(base_type=GloveBaseType.EelskinGloves,        start_level=38, end_level=38),
            ItemProgressionItem(base_type=GloveBaseType.AntiqueGauntlets,     start_level=39, end_level=40),
            ItemProgressionItem(base_type=GloveBaseType.SatinGloves,          start_level=41, end_level=42),
            ItemProgressionItem(base_type=GloveBaseType.SerpentscaleGauntlets,start_level=42, end_level=43),
            ItemProgressionItem(base_type=GloveBaseType.ZealotGloves,         start_level=43, end_level=44),
            ItemProgressionItem(base_type=GloveBaseType.SharkskinGloves,      start_level=44, end_level=45),
            ItemProgressionItem(base_type=GloveBaseType.AmbushMitts,         start_level=45, end_level=46),
            ItemProgressionItem(base_type=GloveBaseType.AncientGauntlets,     start_level=46, end_level=47),
            ItemProgressionItem(base_type=GloveBaseType.SamiteGloves,         start_level=47, end_level=48),
            ItemProgressionItem(base_type=GloveBaseType.WyrmscaleGauntlets,   start_level=49, end_level=49),
            ItemProgressionItem(base_type=GloveBaseType.CarnalMitts,          start_level=50, end_level=50),
            ItemProgressionItem(base_type=GloveBaseType.SoldierGloves,        start_level=51, end_level=52),
            ItemProgressionItem(base_type=GloveBaseType.GoliathGauntlets,     start_level=53, end_level=53),
            ItemProgressionItem(base_type=GloveBaseType.ShagreenGloves,       start_level=54, end_level=54),
            ItemProgressionItem(base_type=GloveBaseType.ConjurerGloves,       start_level=55, end_level=56),
            ItemProgressionItem(base_type=GloveBaseType.LegionGloves,         start_level=57, end_level=57),
            ItemProgressionItem(base_type=GloveBaseType.AssassinsMitts,       start_level=58, end_level=58),
            ItemProgressionItem(base_type=GloveBaseType.HydrascaleGauntlets,  start_level=59, end_level=59),
            ItemProgressionItem(base_type=GloveBaseType.ArcanistGloves,       start_level=60, end_level=61),
            ItemProgressionItem(base_type=GloveBaseType.StealthGloves,        start_level=62, end_level=62),
            ItemProgressionItem(base_type=GloveBaseType.VaalGauntlets,        start_level=63, end_level=65),
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
            ArmorTypeClass.Gloves,
            item_progression_config
        )
