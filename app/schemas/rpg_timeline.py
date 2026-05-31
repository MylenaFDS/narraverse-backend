from pydantic import BaseModel


class RPGTimelineCreate(BaseModel):
    title: str
    content: str | None = None
    date_label: str | None = None


class RPGTimelineUpdate(BaseModel):
    title: str
    content: str | None = None
    date_label: str | None = None


class RPGTimelineResponse(BaseModel):
    id: int
    title: str
    content: str | None
    date_label: str | None

    rpg_id: int
    author_id: int

    class Config:
        from_attributes = True