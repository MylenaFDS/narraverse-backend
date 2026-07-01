from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    character_id = Column(
        Integer,
        ForeignKey("characters.id"),
        nullable=False,
    )

    item_id = Column(
        Integer,
        ForeignKey("items.id"),
        nullable=False,
    )

    quantity = Column(
        Integer,
        default=1,
    )

    equipped = Column(
        Boolean,
        default=False,
    )

    character = relationship(
        "Character"
    )

    item = relationship(
        "Item"
    )