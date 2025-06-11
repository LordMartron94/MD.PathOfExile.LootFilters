from typing import Optional

import pydantic
from pydantic import Field


class CustomAlertSound(pydantic.BaseModel):
    file_name: str
    volume: int = Field(..., ge=0, le=300)
    optional: Optional[bool] = False
