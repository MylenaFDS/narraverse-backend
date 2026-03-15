from pydantic import BaseModel


class CharacterSheetValueCreate(BaseModel):
    field_id: int
    value: str


class CharacterSheetValueResponse(BaseModel):
    id: int
    character_id: int
    field_id: int
    value: str

    class Config:
        from_attributes = True