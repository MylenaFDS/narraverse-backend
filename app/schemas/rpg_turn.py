from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RPGTurnCreate(BaseModel):
    content: str
    mentioned_participants: Optional[List[int]] = []
    reply_to_turn_id: Optional[int] = None
    character_id: Optional [int] = None

class RPGTurnResponse(BaseModel):
    id: int
    content: str
    user_id: int
    character_id: Optional [int] = None
    created_at: datetime
    mentioned_participants: Optional[List[int]] = []
    reply_to_turn_id: Optional[int] = None

    class Config:
        from_attributes = True