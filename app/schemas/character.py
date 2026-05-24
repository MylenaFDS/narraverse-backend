from pydantic import BaseModel
from typing import Optional, List


class SheetValueInput(BaseModel):
    field_id: int
    value: str


class CharacterCreate(BaseModel):
    name: str
    description: Optional[str] = None
    history: str
    world_lore_id: int
    sheet: Optional[List[SheetValueInput]] = []


class CharacterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    history: str
    world_lore_id: int
    user_id: int
    rpg_id: int

    class Config:
        from_attributes = True