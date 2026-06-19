from pydantic import BaseModel


class SceneLocationCreate(BaseModel):
    name: str
    description: str | None = None

    # porcentagem dentro da imagem
    pos_x: int = 50
    pos_y: int = 50

    target_scene_id: int | None = None


class SceneLocationUpdate(BaseModel):
    name: str
    description: str | None = None

    pos_x: int = 50
    pos_y: int = 50

    target_scene_id: int | None = None


class SceneLocationResponse(BaseModel):
    id: int

    name: str
    description: str | None = None

    pos_x: int
    pos_y: int

    scene_id: int
    target_scene_id: int | None = None

    class Config:
        from_attributes = True