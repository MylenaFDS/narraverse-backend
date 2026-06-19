from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class SceneLocation(Base):
    __tablename__ = "scene_locations"

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

    pos_x = Column(
        Integer,
        default=50,
    )

    pos_y = Column(
        Integer,
        default=50,
    )

    scene_id = Column(
        Integer,
        ForeignKey(
            "region_scenes.id"
        ),
        nullable=False,
    )

    target_scene_id = Column(
        Integer,
        ForeignKey(
            "region_scenes.id"
        ),
        nullable=True,
    )

    scene = relationship(
        "RegionScene",
        foreign_keys=[scene_id],
    )

    target_scene = relationship(
        "RegionScene",
        foreign_keys=[target_scene_id],
    )