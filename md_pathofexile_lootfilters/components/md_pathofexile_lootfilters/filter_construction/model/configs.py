from dataclasses import dataclass
from typing import List, Tuple, Dict

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.compiler.model.condition import Condition
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.config.area_lookup import Act
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.style import Style


@dataclass(frozen=True)
class RarityRuleConfig:
    """Configuration for a single rarity’s show‐rules on items."""
    rarity_name: str
    style: Style
    acts: Tuple[Act, Act]
    extra_conditions: List[Condition]


@dataclass(frozen=True)
class ClassRuleConfig:
    """Configuration for class‐level show/hide rules."""
    show_acts: Tuple[Act, Act]
    show_rarities: Dict[str, Style]
    hide_rarities: List[str]
    hide_acts: Tuple[Act, Act]


@dataclass(frozen=True)
class ItemProgressionConfig:
    """All the bits a client needs to decide what to show/hide and where."""
    rarity_rules: List[RarityRuleConfig]
    class_rule: ClassRuleConfig
