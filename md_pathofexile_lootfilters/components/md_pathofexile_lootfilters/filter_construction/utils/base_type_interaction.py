import enum
from typing import List, Union, Sequence

import pandas as pd

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.filter_construction.model.item_progression_item import \
    ItemProgressionItem

class BaseTypeCategory(enum.Enum):
    # WEAPONRY:
    sceptres = "Sceptres"
    shields = "Shields"

    # EQUIPMENT:
    belts = "Belts"
    body_armor = "Body Armor"
    boots = "Boots"
    gloves = "Gloves"
    helmets = "Helmets"

    # FLASKS
    life_flasks = "Life Flasks"
    mana_flasks = "Mana Flasks"
    hybrid_flasks = "Hybrid Flasks"
    utility_flasks = "Utility Flasks"

    # JEWELRY
    rings = "Rings"
    amulets = "Amulets"

    # CURRENCIES
    misc = "Misc Currencies"
    orbs = "Orbs"
    supplies = "Supplies"
    essences = "Essences"

def sanitize_data_columns(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = data.copy()
    cleaned.columns = (
        cleaned.columns
        .str.strip()
        .str.replace(r"\(([^)]+)\)", r"_\1", regex=True)
        .str.replace(r"[-\s]+", "_", regex=True)
        .str.lower()
    )

    return cleaned

def filter_rows_by_category(
        categories: Union[BaseTypeCategory, Sequence[BaseTypeCategory]],
        data: pd.DataFrame
) -> pd.DataFrame:
    """
    Return a DataFrame containing only the rows whose 'Category'
    column matches one or more given BaseTypeCategory values.
    """
    if isinstance(categories, BaseTypeCategory):
        values = [categories.value]
    else:
        values = [cat.value for cat in categories]

    return data[data['Category'].isin(values)]


# noinspection PyUnresolvedReferences
def get_item_progression_for_category(
        category: BaseTypeCategory,
        data: pd.DataFrame
) -> List[ItemProgressionItem]:
    rows = filter_rows_by_category(category, data)
    return [
        ItemProgressionItem(
            base_type=row.BaseType,
            start_level=row.DropLevelStart,
            end_level=row.DropLevelEnd,
            start_area=row.AreaLevelStart,
            end_area=row.AreaLevelEnd
        )
        for row in rows.itertuples(index=False)
    ]
