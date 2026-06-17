from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class RegionPlace(Base):
    __tablename__ = "region_places"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(120),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=False,
    )

    lore = relationship("RPGLore")