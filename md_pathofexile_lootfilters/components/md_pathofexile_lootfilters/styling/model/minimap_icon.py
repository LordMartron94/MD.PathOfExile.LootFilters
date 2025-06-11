import pydantic
from pydantic import Field

from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.styling.utils.literals import ColorLiteral, \
    MinimapShapeLiteral


class MinimapIcon(pydantic.BaseModel):
    size: int = Field(0, ge=0, le=2)
    colour: ColorLiteral = "Red"
    shape: MinimapShapeLiteral = "Star"
