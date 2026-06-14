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

    character_ids: list[int] = []
    faction_ids: list[int] = []


class RPGTimelineUpdate(BaseModel):
    title: str
    content: str | None = None
    date_label: str | None = None

    lore_id: int | None = None
    turn_id: int | None = None
    category_id: int | None = None

    character_ids: list[int] | None = None
    faction_ids: list[int] | None = None


class TimelineLoreResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class TimelineCharacterResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TimelineFactionResponse(BaseModel):
    id: int
    name: str

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

    characters: list[
        TimelineCharacterResponse
    ] = []
    
    factions: list[
    TimelineFactionResponse
    ] = []

    rpg_id: int
    author_id: int

    class Config:
        from_attributes = True