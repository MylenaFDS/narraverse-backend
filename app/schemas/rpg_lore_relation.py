from pydantic import BaseModel


class LoreRelationCreate(BaseModel):
    target_lore_id: int


class LoreRelationResponse(BaseModel):
    id: int

    source_lore_id: int
    target_lore_id: int

    class Config:
        from_attributes = True


class RelatedLoreResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class LoreRelationDetailResponse(BaseModel):
    id: int

    source_lore_id: int
    target_lore_id: int

    target_lore: RelatedLoreResponse

    class Config:
        from_attributes = True