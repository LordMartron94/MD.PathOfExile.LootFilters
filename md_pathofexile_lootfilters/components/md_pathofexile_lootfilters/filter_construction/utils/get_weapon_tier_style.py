from typing import Tuple

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


def determine_styles(data: FilterConstructionPipelineContext) -> Tuple[Style, Style, Style]:
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
