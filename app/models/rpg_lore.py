from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class RPGLore(Base):
    __tablename__ = "rpg_lore"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False, index=True)
    content = Column(Text, nullable=True)

    visual_description = Column(
    Text,
    nullable=True,
    )

    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔥 CONTROLE DE LORE
    is_approved = Column(Boolean, default=False)
    is_suggestion = Column(Boolean, default=False)

    # 🔥 CATEGORIA (continua aqui por compatibilidade)
    category = Column(String(50), default="Geral")

    order = Column(Integer, default=0)

    # RELATIONSHIPS
    rpg = relationship("RPG")
    author = relationship("User")


# ✅ NOVA TABELA
class RPGLoreCategory(Base):
    __tablename__ = "rpg_lore_categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)

    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)

    # RELATIONSHIP
    rpg = relationship("RPG")