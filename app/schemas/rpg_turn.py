from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class RPGTurnCreate(BaseModel):
    content: str

    # NOVO (recomendado)
    mentioned_characters: Optional[List[int]] = Field(default_factory=list)

    # ANTIGO (mantido para não quebrar nada)
    mentioned_participants: Optional[List[int]] = Field(default_factory=list)

    reply_to_turn_id: Optional[int] = None
    character_id: Optional[int] = None


class RPGTurnResponse(BaseModel):
    id: int
    content: str
    user_id: int
    character_id: Optional[int] = None
    created_at: datetime

    # NOVO
    mentioned_characters: Optional[List[int]] = Field(default_factory=list)

    # ANTIGO (compatibilidade)
    mentioned_participants: Optional[List[int]] = Field(default_factory=list)

    reply_to_turn_id: Optional[int] = None

    class Config:
        from_attributes = True