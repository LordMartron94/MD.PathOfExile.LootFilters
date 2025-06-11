from typing import Optional

import pydantic

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral


class PlayEffect(pydantic.BaseModel):
    colour: ColorLiteral = "Red"
    temp: Optional[bool] = False
