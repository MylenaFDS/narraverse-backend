from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from datetime import datetime

from app.db.base import Base


class RPGMessage(Base):
    __tablename__ = "rpg_messages"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)