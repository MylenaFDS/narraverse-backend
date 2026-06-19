from pydantic import BaseModel


class RegionSceneCreate(BaseModel):
    title: str
    description: str | None = None


class RegionSceneUpdate(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None


class RegionSceneResponse(BaseModel):
    id: int

    title: str
    description: str | None = None

    image_url: str | None = None

    is_ai_generated: bool

    lore_id: int

    class Config:
        from_attributes = True