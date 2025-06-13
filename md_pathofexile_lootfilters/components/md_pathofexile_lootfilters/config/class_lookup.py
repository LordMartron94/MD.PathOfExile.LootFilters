import enum
from typing import Dict, List


class WeaponTypeClass(enum.Enum):
    OneHandedAxes = "One Hand Axes"
    OneHandedMaces = "One Hand Maces"
    OneHandedSwords = "One Hand Swords"
    ThrustingOneHandedSwords = "Thrusting One Hand Swords"
    Bows = "Bows"
    Claws = "Claws"
    Daggers = "Daggers"
    Quivers = "Quivers"
    RuneDaggers = "Rune Daggers"
    Sceptres = "Sceptres"
    Shields = "Shields"
    Staves = "Staves"
    TwoHandedAxes = "Two Hand Axes"
    TwoHandedMaces = "Two Hand Maces"
    TwoHandedSwords = "Two Hand Swords"
    Wands = "Wands"
    Warstaves = "Warstaves"

class ArmorTypeClass(enum.Enum):
    Belts = "Belts"
    Boots = "Boots"
    Gloves = "Gloves"
    BodyArmor = "Body Armours"
    Helmets = "Helmets"

class FlaskTypeClass(enum.Enum):
    Life = "Life Flasks"
    Mana = "Mana Flasks"
    Hybrid = "Hybrid Flasks"
    Utility = "Utility Flasks"

class OtherTypeClass(enum.Enum):
    Tincture = "Tinctures"


class BuildType(enum.Enum):
    MeleeSpellcaster = "Melee Spellcaster"


_ASSOCIATED_WEAPONS_LOOKUP: Dict[BuildType, List[WeaponTypeClass]] = {
    BuildType.MeleeSpellcaster: [
        WeaponTypeClass.Sceptres,
        WeaponTypeClass.Shields,
    ]
}


def get_associated_weapons(build_type: BuildType) -> List[WeaponTypeClass]:
    """
    Return the list of EquipmentTypes associated with a given BuildType.
    """
    return _ASSOCIATED_WEAPONS_LOOKUP.get(build_type, [])


def get_unassociated_weapons(build_type: BuildType) -> List[WeaponTypeClass]:
    """
    Return the list of EquipmentTypes not associated with the given BuildType.
    """
    associated = set(get_associated_weapons(build_type))
    return [equip for equip in WeaponTypeClass if equip not in associated]
