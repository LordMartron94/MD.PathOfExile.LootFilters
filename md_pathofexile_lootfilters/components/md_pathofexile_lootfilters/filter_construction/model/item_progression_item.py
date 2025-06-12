import enum
from typing import Optional

import pydantic


class ItemProgressionItem(pydantic.BaseModel):
    base_type: enum.Enum
    start_level: Optional[int] = None
    end_level: Optional[int] = None
    start_area: Optional[int] = None
    end_area: Optional[int] = None
