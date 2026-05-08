from pydantic import BaseModel


class MapRegionCreate(BaseModel):
    name: str
    description: str | None = None
    x: int
    y: int


class MapRegionResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    x: int
    y: int
    rpg_id: int

    class Config:
        from_attributes = True