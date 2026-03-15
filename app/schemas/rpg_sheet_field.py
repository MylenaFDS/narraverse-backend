from pydantic import BaseModel


class RPGSheetFieldCreate(BaseModel):
    name: str
    field_type: str = "text"


class RPGSheetFieldResponse(BaseModel):
    id: int
    name: str
    field_type: str
    rpg_id: int

    class Config:
        from_attributes = True