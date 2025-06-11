import enum

import pydantic


class ItemProgressionItem(pydantic.BaseModel):
    base_type: enum.Enum
    start_level: int
    end_level: int
