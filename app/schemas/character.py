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
    image_url: Optional[str] = None


class CharacterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    history: Optional[str] = None
    world_lore_id: Optional[int] = None
    user_id: int
    rpg_id: int
    image_url: Optional[str] = None
    class Config:
        from_attributes = True