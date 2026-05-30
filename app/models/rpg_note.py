from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class RPGNote(Base):
    __tablename__ = "rpg_notes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=True)
    content = Column(Text, nullable=True)

    is_pinned = Column(Boolean, default=False, nullable=False)

    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    rpg = relationship("RPG")
    author = relationship("User")