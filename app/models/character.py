from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.db.base import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(120), nullable=False, index=True)
    description = Column(Text, nullable=True)
    sheet = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False, index=True)

    owner = relationship("User")

    rpg = relationship("RPG")

    __table_args__ = (
        Index("idx_character_rpg_user", "rpg_id", "user_id"),
    )