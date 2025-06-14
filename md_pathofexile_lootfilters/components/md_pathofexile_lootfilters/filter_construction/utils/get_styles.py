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

_MAPPING = {
    "Normal": ItemTier.LowTier1,
    "Magic": ItemTier.MidTier3,
    "Rare": ItemTier.MidTier1,
    "Unique": ItemTier.HighTier1
}

def get_weaponry_and_equipment_tier(rarity: str) -> ItemTier:
    return _MAPPING[rarity]

def determine_weaponry_and_equipment_styles(data: FilterConstructionPipelineContext) -> Tuple[Style, Style, Style, Style]:
    normal = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        get_weaponry_and_equipment_tier("Normal")
    )

    magic = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        get_weaponry_and_equipment_tier("Magic")
    )

    rare = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        get_weaponry_and_equipment_tier("Rare")
    )

    unique = data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        get_weaponry_and_equipment_tier("Unique")
    )

    return normal, magic, rare, unique

def get_weapon_style_from_tier(data: FilterConstructionPipelineContext, tier: ItemTier) -> Style:
    return data.style_preset_registry.get_style(
        ItemGroup.WeaponryAndEquipment,
        tier
    )

def determine_flask_style(data: FilterConstructionPipelineContext, is_utility_flask: bool = False) -> Style:
    if is_utility_flask:
        return data.style_preset_registry.get_style(ItemGroup.Flasks, ItemTier.HighTier2)

    return data.style_preset_registry.get_style(ItemGroup.Flasks, ItemTier.HighTier3)

def determine_style(data: FilterConstructionPipelineContext, tier: ItemTier, base_type_category: BaseTypeCategory) -> Style:
    mapping = {
        BaseTypeCategory.supplies: ItemGroup.Supplies,
        BaseTypeCategory.misc: ItemGroup.MiscCurrencies,
        BaseTypeCategory.essences: ItemGroup.Essences,
        BaseTypeCategory.rings: ItemGroup.Jewelry,
        BaseTypeCategory.amulets: ItemGroup.Jewelry,
        BaseTypeCategory.orbs: ItemGroup.Orbs,
        BaseTypeCategory.gold: ItemGroup.Gold,
        BaseTypeCategory.skill_gems: ItemGroup.SkillGems,
        BaseTypeCategory.vendor_recipes: ItemGroup.VendorRecipes
    }

    group = mapping.get(base_type_category, None)

    if group is None:
        raise RuntimeError(f"Unknown currency type {base_type_category}")

    return data.style_preset_registry.get_style(
        group,
        tier
    )
