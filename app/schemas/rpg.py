from pydantic import BaseModel


class RPGCreate(BaseModel):
    name: str
    description: str | None = None


class RPGResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True