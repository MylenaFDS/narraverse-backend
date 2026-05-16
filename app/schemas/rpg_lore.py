from pydantic import BaseModel
from typing import Optional


class RPGLoreCreate(BaseModel):
    title: str
    content: str
    category: str


class RPGLoreUpdate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None


class RPGLoreResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str] = None
    author_id: int
    is_approved: bool
    is_suggestion: bool

    class Config:
        from_attributes = True