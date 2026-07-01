from pydantic import BaseModel
from typing import Optional, List

from app.schemas.character_sheet import (
    CharacterSheetValueResponse,
)


class SheetValueInput(BaseModel):
    field_id: int
    value: str


class CharacterCreate(BaseModel):
    name: str

    description: Optional[str] = None

    history: str

    world_lore_id: int

    faction_id: Optional[int] = None

    sheet: Optional[List[SheetValueInput]] = []

    image_url: Optional[str] = None

    is_npc: bool = False


# ===========================
# Facção
# ===========================

class CharacterFactionResponse(BaseModel):
    id: int

    name: str

    class Config:
        from_attributes = True


# ===========================
# Response
# ===========================

class CharacterResponse(BaseModel):
    id: int

    name: str

    description: Optional[str] = None

    history: Optional[str] = None

    world_lore_id: Optional[int] = None

    faction_id: Optional[int] = None

    faction: Optional[
        CharacterFactionResponse
    ] = None

    user_id: int

    rpg_id: int

    image_url: Optional[str] = None

    is_npc: bool

    sheet_values: List[
        CharacterSheetValueResponse
    ] = []

    class Config:
        from_attributes = True