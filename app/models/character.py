from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ==========================
    # Dados básicos
    # ==========================

    name = Column(
        String(120),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    history = Column(
        Text,
        nullable=True,
    )

    image_url = Column(
        String,
        nullable=True,
    )

    # ==========================
    # NPC
    # ==========================

    is_npc = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==========================
    # Mundo
    # ==========================

    world_lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=True,
    )

    faction_id = Column(
        Integer,
        ForeignKey("rpg_factions.id"),
        nullable=True,
    )

    # ==========================
    # Compatibilidade antiga
    # ==========================

    sheet = Column(
        Text,
        nullable=True,
    )

    # ==========================
    # Relacionamentos
    # ==========================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        nullable=False,
    )

    owner = relationship(
        "User"
    )

    rpg = relationship(
        "RPG"
    )

    world_lore = relationship(
        "RPGLore"
    )

    faction = relationship(
        "RPGFaction"
    )

    sheet_values = relationship(
        "CharacterSheetValue",
        back_populates="character",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "idx_character_rpg_user",
            "rpg_id",
            "user_id",
        ),
    )