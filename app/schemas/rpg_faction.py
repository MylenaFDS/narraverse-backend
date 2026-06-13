from pydantic import BaseModel


class RPGFactionCreate(BaseModel):
    name: str
    description: str | None = None


class RPGFactionUpdate(BaseModel):
    name: str
    description: str | None = None


class RPGFactionResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    rpg_id: int

    class Config:
        from_attributes = True