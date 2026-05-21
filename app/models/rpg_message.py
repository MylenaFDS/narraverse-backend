from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class RPGMessage(Base):
    __tablename__ = "rpg_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        nullable=False
    )

    # 🔥 NOVO
    reply_to_message_id = Column(
        Integer,
        ForeignKey("rpg_messages.id"),
        nullable=True
    )

    # 🔥 relação da mensagem respondida
    reply_to = relationship(
        "RPGMessage",
        remote_side=[id],
        lazy="joined"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )