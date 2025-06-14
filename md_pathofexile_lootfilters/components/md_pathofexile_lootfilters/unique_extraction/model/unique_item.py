from dataclasses import dataclass


@dataclass
class UniqueItem:
    name: str
    base_type: str
    listing_count: int
    count: int
    rarity: int = 0
