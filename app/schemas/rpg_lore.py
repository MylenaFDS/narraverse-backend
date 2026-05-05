from pydantic import BaseModel


class RPGLoreCreate(BaseModel):
    title: str
    content: str
    category: str


class RPGLoreResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    author_id: int
    is_approved: bool
    is_suggestion: bool

    class Config:
        from_attributes = True