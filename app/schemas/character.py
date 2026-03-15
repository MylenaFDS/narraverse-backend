from pydantic import BaseModel
from typing import Optional


class CharacterCreate(BaseModel):
    name: str
    description: Optional[str] = None
    sheet: Optional[str] = None


class CharacterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    sheet: Optional[str]
    user_id: int
    rpg_id: int

    class Config:
        from_attributes = True