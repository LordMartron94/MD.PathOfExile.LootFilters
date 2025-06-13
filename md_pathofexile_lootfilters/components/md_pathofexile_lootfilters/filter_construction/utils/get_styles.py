from typing import Tuple, Dict

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.jewelry_base_type import RingBaseType, \
    AmuletBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.base_types.orb_base_type import OrbBaseType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_group import \
    ItemGroup
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.item_classifiers.item_tier import \
    ItemTier, get_new_tier
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.pipeline.pipeline_context import \
    FilterConstructionPipelineContext
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

def determine_ring_style(
        data: FilterConstructionPipelineContext,
        ring_base: RingBaseType,
        rarity: str,
) -> Tuple[Style, ItemTier]:
    # 1) map each base to its default (Normal) tier
    base_tier_map: Dict[RingBaseType, ItemTier] = {
        # HIGH
        RingBaseType.Unset:    ItemTier.HighTier2,
        RingBaseType.Breach:   ItemTier.HighTier3,
        RingBaseType.Gold:     ItemTier.HighTier3,
        RingBaseType.Diamond:  ItemTier.HighTier3,
        RingBaseType.Amethyst: ItemTier.HighTier3,

        # MID
        RingBaseType.Sapphire: ItemTier.MidTier1,
        RingBaseType.Topaz:    ItemTier.MidTier1,
        RingBaseType.Ruby:     ItemTier.MidTier1,
        RingBaseType.TwoStone: ItemTier.MidTier1,
        RingBaseType.Prismatic:ItemTier.MidTier1,

        RingBaseType.Coral:    ItemTier.MidTier2,
        RingBaseType.Paua:     ItemTier.MidTier2,
        RingBaseType.Moonstone:ItemTier.MidTier2,
        RingBaseType.Bone:     ItemTier.MidTier2,

        # LOW
        RingBaseType.Iron:     ItemTier.LowTier3,
    }

    base_tier = base_tier_map.get(ring_base, None)
    if base_tier is None:
        raise RuntimeError(f"No default tier for ring {ring_base}")

    final_tier = get_new_tier(base_tier, rarity)

    # 2) fetch style
    return data.style_preset_registry.get_style(
        ItemGroup.Jewelry,
        final_tier
    ), final_tier

def determine_amulet_style(
        data: FilterConstructionPipelineContext,
        amulet_base: AmuletBaseType,
        rarity: str,
) -> Tuple[Style, ItemTier]:
    # 1) map each base to its default (Normal) tier
    base_tier_map: Dict[AmuletBaseType, ItemTier] = {
        # HIGH
        AmuletBaseType.Gold:   ItemTier.HighTier3,

        # MID
        AmuletBaseType.Onyx: ItemTier.MidTier1,
        AmuletBaseType.Agate:ItemTier.MidTier1,

        AmuletBaseType.Citrine:    ItemTier.MidTier2,
        AmuletBaseType.Turquoise:    ItemTier.MidTier2,
        AmuletBaseType.Amber:    ItemTier.MidTier2,
        AmuletBaseType.Lapis:    ItemTier.MidTier2,
        AmuletBaseType.Paua:     ItemTier.MidTier2,

        AmuletBaseType.Jade:     ItemTier.MidTier3,

        # LOW
        AmuletBaseType.Coral:    ItemTier.LowTier2,
    }

    base_tier = base_tier_map.get(amulet_base, None)
    if base_tier is None:
        raise RuntimeError(f"No default tier for amulet {amulet_base}")

    final_tier = get_new_tier(base_tier, rarity)

    # 2) fetch style
    return data.style_preset_registry.get_style(
        ItemGroup.Jewelry,
        final_tier
    ), final_tier

def determine_orb_style(data: FilterConstructionPipelineContext, orb_base: OrbBaseType) -> Tuple[Style, ItemTier]:
    base_tier_map: Dict[OrbBaseType, ItemTier] = {
        # GOD
        OrbBaseType.Vaal: ItemTier.GodTier3,

        # HIGH
        OrbBaseType.Exalted: ItemTier.HighTier1,
        OrbBaseType.Regret: ItemTier.HighTier1,
        OrbBaseType.Chaos: ItemTier.HighTier1,

        OrbBaseType.Regal: ItemTier.HighTier2,
        OrbBaseType.Binding: ItemTier.HighTier2,

        OrbBaseType.Alchemy: ItemTier.HighTier3,

        # MID
        OrbBaseType.Chromatic: ItemTier.MidTier1,
        OrbBaseType.Jewellers: ItemTier.MidTier1,
        OrbBaseType.Fusing: ItemTier.MidTier1,
        OrbBaseType.Scouring: ItemTier.MidTier1,

        OrbBaseType.Chance: ItemTier.MidTier2,

        OrbBaseType.Alteration: ItemTier.MidTier3,

        # LOW
        OrbBaseType.Augmentation: ItemTier.LowTier1,
        OrbBaseType.Transmutation: ItemTier.LowTier1
    }

    tier = base_tier_map.get(orb_base, None)
    if tier is None:
        raise RuntimeError(f"No default tier for orb {orb_base}")

    return data.style_preset_registry.get_style(
        ItemGroup.Orbs,
        tier
    ), tier
