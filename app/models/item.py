from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    JSON,
)

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    category = Column(
        String(50),
        nullable=False,
    )

    rarity = Column(
        String(30),
        default="common",
    )

    weight = Column(
        Integer,
        default=0,
    )

    value = Column(
        Integer,
        default=0,
    )

    modifiers = Column(
        JSON,
        nullable=True,
    )