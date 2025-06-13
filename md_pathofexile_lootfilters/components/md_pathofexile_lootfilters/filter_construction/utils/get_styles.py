from typing import Tuple

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.utils.base_type_interaction import \
    BaseTypeCategory
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


def determine_weaponry_and_equipment_styles(data: FilterConstructionPipelineContext) -> Tuple[Style, Style, Style, Style]:
    normal = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        ItemTier.LowTier1
    )

    magic = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        ItemTier.MidTier3
    )

    rare = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        ItemTier.MidTier1
    )

    unique = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        ItemTier.HighTier1
    )

    return normal, magic, rare, unique

def determine_flask_style(data: FilterConstructionPipelineContext, is_utility_flask: bool = False) -> Style:
    if is_utility_flask:
        return data.style_preset_registry.get_style(ItemGroup.Flasks, ItemTier.HighTier2)

    return data.style_preset_registry.get_style(ItemGroup.Flasks, ItemTier.HighTier3)

def determine_style(data: FilterConstructionPipelineContext, tier: ItemTier, currency_type: BaseTypeCategory) -> Style:
    mapping = {
        BaseTypeCategory.supplies: ItemGroup.Supplies,
        BaseTypeCategory.misc: ItemGroup.MiscCurrencies,
        BaseTypeCategory.essences: ItemGroup.Essences,
        BaseTypeCategory.rings: ItemGroup.Jewelry,
        BaseTypeCategory.amulets: ItemGroup.Jewelry,
        BaseTypeCategory.orbs: ItemGroup.Orbs,
        BaseTypeCategory.gold: ItemGroup.Gold,
        BaseTypeCategory.skill_gems: ItemGroup.SkillGems,
    }

    group = mapping.get(currency_type, None)

    if group is None:
        raise RuntimeError(f"Unknown currency type {currency_type}")

    return data.style_preset_registry.get_style(
        group,
        tier
    )
