from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class RPGTimeline(Base):
    __tablename__ = "rpg_timeline"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=True,
    )

    date_label = Column(
        String(100),
        nullable=True,
    )

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        nullable=False,
    )

    author_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )


    rpg = relationship("RPG")
    author = relationship("User")