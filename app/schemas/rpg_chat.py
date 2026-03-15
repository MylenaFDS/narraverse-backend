from pydantic import BaseModel
from datetime import datetime


class RPGChatMessageCreate(BaseModel):
    content: str


class RPGChatMessageResponse(BaseModel):
    id: int
    content: str
    user_id: int
    rpg_id: int
    created_at: datetime

    class Config:
        from_attributes = True