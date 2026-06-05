from pydantic import BaseModel
from app.schemas.rpg_timeline_category import (
    TimelineCategoryResponse,
)


class RPGTimelineCreate(BaseModel):
    title: str
    content: str | None = None
    date_label: str | None = None
    lore_id: int | None = None
    turn_id: int | None = None
    category_id: int | None = None


class RPGTimelineUpdate(BaseModel):
    title: str
    content: str | None = None
    date_label: str | None = None
    lore_id: int | None = None
    turn_id: int | None = None
    category_id: int | None = None

class TimelineLoreResponse(BaseModel):
    id: int
    title: str
   
    class Config:
        from_attributes = True


class RPGTimelineResponse(BaseModel):
    id: int
    title: str
    content: str | None
    date_label: str | None
    turn_id: int | None = None
    category_id: int | None = None
    category: TimelineCategoryResponse | None = None
    lore_id: int | None = None
    lore: TimelineLoreResponse | None = None

    rpg_id: int
    author_id: int

    class Config:
        from_attributes = True