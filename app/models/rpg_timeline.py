from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Table,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


timeline_characters = Table(
    "rpg_timeline_characters",
    Base.metadata,
    Column(
        "timeline_id",
        Integer,
        ForeignKey("rpg_timeline.id"),
        primary_key=True,
    ),
    Column(
        "character_id",
        Integer,
        ForeignKey("characters.id"),
        primary_key=True,
    ),
)


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

    lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=True,
    )

    turn_id = Column(
        Integer,
        ForeignKey("rpg_turns.id"),
        nullable=True,
    )

    category_id = Column(
        Integer,
        ForeignKey(
            "rpg_timeline_categories.id"
        ),
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
    lore = relationship("RPGLore")
    turn = relationship("RPGTurn")
    category = relationship(
        "RPGTimelineCategory"
    )

    characters = relationship(
        "Character",
        secondary=timeline_characters,
    )