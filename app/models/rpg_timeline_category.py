from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class RPGTimelineCategory(Base):
    __tablename__ = (
        "rpg_timeline_categories"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        nullable=False,
    )

    rpg = relationship("RPG")