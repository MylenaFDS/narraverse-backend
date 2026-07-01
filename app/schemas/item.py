from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):

    name: str

    description: Optional[str] = None

    category: str

    rarity: str = "common"

    weight: int = 0

    value: int = 0

    modifiers: dict = {}


class ItemResponse(ItemCreate):

    id: int

    class Config:
        from_attributes = True