from pydantic import BaseModel


class TimelineCategoryCreate(
    BaseModel
):
    name: str


class TimelineCategoryResponse(
    BaseModel
):
    id: int
    name: str
    rpg_id: int

    class Config:
        from_attributes = True