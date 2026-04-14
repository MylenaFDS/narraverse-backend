from pydantic import BaseModel
from typing import Optional, List


class SheetValueInput(BaseModel):
    field_id: int
    value: str


class CharacterCreate(BaseModel):
    name: str
    description: Optional[str] = None
    sheet: Optional[List[SheetValueInput]] = []


class CharacterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    rpg_id: int

    class Config:
        from_attributes = True