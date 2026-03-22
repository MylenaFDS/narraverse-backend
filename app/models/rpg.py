from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.models.rpg_tag import rpg_tags


class RPG(Base):
    __tablename__ = "rpgs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # CONFIGURAÇÕES DO RPG (definidas pelo criador)

    has_gm = Column(Boolean, default=False)  # RPG possui mestre
    allow_chat = Column(Boolean, default=True)  # existe chat separado
    allow_character_sheets = Column(Boolean, default=True)  # permite fichas
    allow_join_requests = Column(Boolean, default=True)  # usuários podem pedir entrada
    allow_free_turns = Column(Boolean, default=True)
    allow_lore_suggestions = Column(Boolean, default=False)

    # sistema de turnos
    turn_mode = Column(
        String(20),
        default="free"
    )
    # opções possíveis:
    # "free" = turnos livres estilo fórum
    # "ordered" = ordem de turnos definida

    # RELACIONAMENTOS

    owner = relationship(
        "User",
        back_populates="owned_rpgs"
    )

    participants = relationship(
        "RPGParticipant",
        back_populates="rpg",
        cascade="all, delete-orphan"
    )

    tags = relationship("Tag", secondary=rpg_tags, backref="rpgs")