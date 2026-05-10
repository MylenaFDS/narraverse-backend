from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.rpg_tag import rpg_tags


class RPG(Base):
    __tablename__ = "rpgs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # 🗺️ MAPA DO MUNDO
    world_map = Column(String, nullable=True)
    map_regions = relationship(
    "MapRegion",
    back_populates="rpg",
    cascade="all, delete-orphan"
)
    # 🔥 APENAS UM DONO
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="owned_rpgs")

    # CONFIGURAÇÕES
    has_gm = Column(Boolean, default=False)
    allow_chat = Column(Boolean, default=True)
    allow_character_sheets = Column(Boolean, default=True)
    allow_join_requests = Column(Boolean, default=True)
    allow_free_turns = Column(Boolean, default=True)
    allow_lore_suggestions = Column(Boolean, default=False)

    turn_mode = Column(String(20), default="free")

    participants = relationship(
        "RPGParticipant",
        back_populates="rpg",
        cascade="all, delete-orphan"
    )

    tags = relationship("Tag", secondary=rpg_tags, backref="rpgs")