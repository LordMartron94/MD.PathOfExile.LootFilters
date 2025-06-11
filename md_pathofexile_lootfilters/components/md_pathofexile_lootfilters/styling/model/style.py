from typing import Optional

import pydantic
from pydantic import Field

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.color import Color
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.minimap_icon import MinimapIcon
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.model.play_effect import PlayEffect


class Style(pydantic.BaseModel):
    minimap_icon: Optional[MinimapIcon] = None
    play_effect: Optional[PlayEffect] = None

    background_color: Color
    border_color: Color
    text_color: Color

    font_size: int = Field(..., ge=1, le=45)
