from pydantic import BaseModel


class RPGSheetFieldCreate(BaseModel):
    name: str
    field_type: str = "text"
    category: str | None = None


class RPGSheetFieldResponse(BaseModel):
    id: int
    rpg_id: int
    name: str
    field_type: str
    category: str | None = None

    class Config:
        from_attributes = True