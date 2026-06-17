from pydantic import BaseModel


class RegionPlaceCreate(BaseModel):
    name: str
    description: str | None = None


class RegionPlaceUpdate(BaseModel):
    name: str
    description: str | None = None


class RegionPlaceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    lore_id: int

    class Config:
        from_attributes = True