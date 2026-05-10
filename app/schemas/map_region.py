from pydantic import BaseModel


class MapRegionCreate(BaseModel):
    name: str

    lore_id: int | None = None

    pos_x: int
    pos_y: int

    color: str = "#7c3aed"


class MapRegionResponse(BaseModel):
    id: int

    name: str

    lore_id: int | None = None

    pos_x: int
    pos_y: int

    color: str

    rpg_id: int

    class Config:
        from_attributes = True