from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class RegionScene(Base):
    __tablename__ = "region_scenes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(120),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    image_url = Column(
        String,
        nullable=True,
    )

    is_ai_generated = Column(
        Boolean,
        default=False,
    )

    lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=False,
    )

    lore = relationship("RPGLore")