import enum
from typing import Dict, List


class EquipmentType(enum.Enum):
    OneHandedAxes = "One Hand Axes"
    OneHandedMaces = "One Hand Maces"
    OneHandedSwords = "One Hand Swords"
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


class BuildType(enum.Enum):
    MeleeSpellcaster = "Melee Spellcaster"


_ASSOCIATED_EQUIPMENTS_LOOKUP: Dict[BuildType, List[EquipmentType]] = {
    BuildType.MeleeSpellcaster: [
        EquipmentType.Sceptres,
        EquipmentType.Shields,
        EquipmentType.RuneDaggers
    ]
}


def get_associated_equipments(build_type: BuildType) -> List[EquipmentType]:
    """
    Return the list of EquipmentTypes associated with a given BuildType.
    """
    return _ASSOCIATED_EQUIPMENTS_LOOKUP.get(build_type, [])


def get_unassociated_equipments(build_type: BuildType) -> List[EquipmentType]:
    """
    Return the list of EquipmentTypes not associated with the given BuildType.
    """
    associated = set(get_associated_equipments(build_type))
    return [equip for equip in EquipmentType if equip not in associated]
