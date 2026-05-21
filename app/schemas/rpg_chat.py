from pydantic import BaseModel
from datetime import datetime


# ===============================
# REPLY
# ===============================
class ReplyMessage(BaseModel):
    id: int
    content: str
    username: str

    class Config:
        from_attributes = True


# ===============================
# CREATE
# ===============================
class RPGChatMessageCreate(BaseModel):
    content: str
    reply_to_message_id: int | None = None


# ===============================
# RESPONSE
# ===============================
class RPGChatMessageResponse(BaseModel):
    id: int
    content: str
    user_id: int
    rpg_id: int
    created_at: datetime

    # 🔥 NOVOS
    username: str | None = None
    reply_to_message_id: int | None = None
    reply_to: ReplyMessage | None = None

    class Config:
        from_attributes = True