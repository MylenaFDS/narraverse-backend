from pydantic import BaseModel
from typing import List, Optional


class RPGCreate(BaseModel):
    name: str
    description: Optional[str] = None
    allow_join_requests: bool = True
    tags: Optional[List[str]] = []
    banner_url: str | None = None

class RPGInvite(BaseModel):
    user_id: int

class RPGResponse(BaseModel):
    id: int
    name: str
    description: str | None
    banner_url: str | None = None
    tags: list[str] = []
    owner_id: int
    is_owner: bool
   
    # 🔥 ADICIONAR
    world_map: str | None = None

    class Config:
        from_attributes = True