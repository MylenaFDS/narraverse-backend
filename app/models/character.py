from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.db.base import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    history = Column(Text, nullable=True)

    world_lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=True
    )

    image_url = Column(String, nullable=True)
    
    # ⚠️ mantém por compatibilidade (pode remover depois com migração)
    sheet = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)

    owner = relationship("User")
    rpg = relationship("RPG")

    # 🔥 NOVO
    sheet_values = relationship("CharacterSheetValue", back_populates="character")
    world_lore = relationship("RPGLore")

    __table_args__ = (
        Index("idx_character_rpg_user", "rpg_id", "user_id"),
    )