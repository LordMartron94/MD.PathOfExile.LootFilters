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


def determine_weaponry_and_equipment_styles(data: FilterConstructionPipelineContext) -> Tuple[Style, Style, Style]:
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

    return normal, magic, rare

def determine_flask_style(data: FilterConstructionPipelineContext, is_utility_flask: bool = False) -> Style:
    if is_utility_flask:
        return data.style_preset_registry.get_style(ItemGroup.Flasks, ItemTier.HighTier2)

    return data.style_preset_registry.get_style(ItemGroup.Flasks, ItemTier.HighTier3)

def determine_jewelry_style(
        data: FilterConstructionPipelineContext,
        tier: ItemTier
) -> Style:
    return data.style_preset_registry.get_style(
        ItemGroup.Jewelry,
        tier
    )

def determine_orb_style(data: FilterConstructionPipelineContext, tier: ItemTier) -> Style:
    return data.style_preset_registry.get_style(
        ItemGroup.Orbs,
        tier
    )

def determine_currency_style(data: FilterConstructionPipelineContext, tier: ItemTier, currency_type: BaseTypeCategory) -> Style:
    return data.style_preset_registry.get_style(
        ItemGroup.Supplies if currency_type == BaseTypeCategory.supplies else ItemGroup.MiscCurrencies,
        tier
    )
