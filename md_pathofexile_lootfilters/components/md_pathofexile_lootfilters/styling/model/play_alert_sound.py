from typing import Optional

import pydantic
from pydantic import Field


class PlayAlertSound(pydantic.BaseModel):
    id: int = Field(..., ge=1, le=16)
    volume: int = Field(..., ge=0, le=300)
    positional: Optional[bool] = False
