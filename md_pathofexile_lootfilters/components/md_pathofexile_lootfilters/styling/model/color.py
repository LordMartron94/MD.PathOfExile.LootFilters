import pydantic
from pydantic import Field


class Color(pydantic.BaseModel):
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)
    alpha: int = Field(..., ge=0, le=255)
