from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class RPGFaction(Base):
    __tablename__ = "rpg_factions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        nullable=False,
    )

    rpg = relationship("RPG")