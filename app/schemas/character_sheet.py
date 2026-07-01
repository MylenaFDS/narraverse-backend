from pydantic import BaseModel


class CharacterSheetValueCreate(BaseModel):
    field_id: int
    value: str


# ===========================
# Campo da ficha
# ===========================

class RPGSheetFieldSimple(BaseModel):
    id: int

    name: str

    field_type: str

    class Config:
        from_attributes = True


# ===========================
# Valor da ficha
# ===========================

class CharacterSheetValueResponse(BaseModel):
    id: int

    value: str

    field: RPGSheetFieldSimple

    class Config:
        from_attributes = True