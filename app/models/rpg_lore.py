from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class RPGLore(Base):
    __tablename__ = "rpg_lore"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=True)

    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔥 CONTROLE DE LORE
    is_approved = Column(Boolean, default=False)
    is_suggestion = Column(Boolean, default=False)

    # RELATIONSHIPS
    rpg = relationship("RPG")
    author = relationship("User")