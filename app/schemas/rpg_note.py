from pydantic import BaseModel


class RPGNoteCreate(BaseModel):
    title: str | None = None
    content: str | None = None


class RPGNoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_pinned: bool | None = None


class RPGNoteResponse(BaseModel):
    id: int
    title: str | None
    content: str | None
    rpg_id: int
    author_id: int
    is_pinned: bool

    class Config:
        from_attributes = True