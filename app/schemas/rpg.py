from pydantic import BaseModel
from typing import List, Optional


class RPGCreate(BaseModel):
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = []


class RPGResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    is_owner: bool
    class Config:
        from_attributes = True