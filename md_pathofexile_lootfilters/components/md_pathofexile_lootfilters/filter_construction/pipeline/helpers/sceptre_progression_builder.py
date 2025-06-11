from typing import List

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.sceptre_base_type import \
    SceptreBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.block_type import RuleType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.factory.condition_group_factory import \
    ConditionGroupFactory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import ConditionKeyWord
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.rule import Rule
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.class_lookup import WeaponTypeClass
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.item_progression_builder import \
    ItemProgressionBuilder
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style

class SceptreProgressionBuilder:
    def __init__(self):
        self._builder = ItemProgressionBuilder()

        self._item_progression: List[ItemProgressionItem] = [
            ItemProgressionItem(base_type=SceptreBaseType.DriftwoodSceptre, start_level=1, end_level=4),
            ItemProgressionItem(base_type=SceptreBaseType.DarkwoodSceptre,  start_level=5, end_level=9),
            ItemProgressionItem(base_type=SceptreBaseType.BronzeSceptre,    start_level=10, end_level=14),
            ItemProgressionItem(base_type=SceptreBaseType.QuartzSceptre,    start_level=15, end_level=19),
            ItemProgressionItem(base_type=SceptreBaseType.IronSceptre,      start_level=20, end_level=23),
            ItemProgressionItem(base_type=SceptreBaseType.OchreSceptre,     start_level=24, end_level=27),
            ItemProgressionItem(base_type=SceptreBaseType.RitualSceptre,    start_level=28, end_level=31),
            ItemProgressionItem(base_type=SceptreBaseType.ShadowSceptre,    start_level=32, end_level=34),
            ItemProgressionItem(base_type=SceptreBaseType.GrinningFetish,   start_level=35, end_level=35),
            ItemProgressionItem(base_type=SceptreBaseType.HornedSceptre,    start_level=36, end_level=37),
            ItemProgressionItem(base_type=SceptreBaseType.Sekhem,           start_level=38, end_level=40),
            ItemProgressionItem(base_type=SceptreBaseType.CrystalSceptre,   start_level=41, end_level=43),
            ItemProgressionItem(base_type=SceptreBaseType.LeadSceptre,      start_level=44, end_level=46),
            ItemProgressionItem(base_type=SceptreBaseType.BloodSceptre,     start_level=47, end_level=49),
            ItemProgressionItem(base_type=SceptreBaseType.RoyalSceptre,     start_level=50, end_level=52),
            ItemProgressionItem(base_type=SceptreBaseType.AbyssalSceptre,   start_level=53, end_level=54),
            ItemProgressionItem(base_type=SceptreBaseType.StagSceptre,      start_level=55, end_level=55),
            ItemProgressionItem(base_type=SceptreBaseType.KaruiSceptre,     start_level=56, end_level=57),
            ItemProgressionItem(base_type=SceptreBaseType.TyrantSekhem,     start_level=58, end_level=59),
            ItemProgressionItem(base_type=SceptreBaseType.OpalSceptre,      start_level=60, end_level=61),
            ItemProgressionItem(base_type=SceptreBaseType.PlatinumSceptre,  start_level=62, end_level=63),
            ItemProgressionItem(base_type=SceptreBaseType.VaalSceptre,      start_level=64, end_level=65),
        ]

    def get_progression_rules(self, data: FilterConstructionPipelineContext) -> List[Rule]:
        style = self._determine_style(data)
        rules = self._builder.get_progression_rules(data.condition_factory, data.rule_factory, self._item_progression, style, style, style)

        exclude_condition = data.condition_factory.create_condition(ConditionKeyWord.Class, operator=None, value=WeaponTypeClass.Sceptres.value)
        rarity_conditions = ConditionGroupFactory.from_exact_values(
            data.condition_factory,
            ConditionKeyWord.Rarity,
            values=["Normal", "Magic", "Rare"]
        )
        area_conditions = ConditionGroupFactory.between_acts(
            data.condition_factory,
            Act.Act1,
            Act.Act10
        )

        exclude_rule = data.rule_factory.get_rule(RuleType.HIDE,  area_conditions + rarity_conditions + [exclude_condition], None)

        rules.append(exclude_rule)
        return rules

    @staticmethod
    def _determine_style(data: FilterConstructionPipelineContext) -> Style:
        return data.style_preset_registry.get_style(
            ItemGroup.EarlyWeaponry,
            ItemTier.NoTier
        )
