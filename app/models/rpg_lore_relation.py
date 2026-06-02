from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class RPGLoreRelation(Base):
    __tablename__ = "rpg_lore_relations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    source_lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=False,
    )

    target_lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=False,
    )

    source_lore = relationship(
        "RPGLore",
        foreign_keys=[source_lore_id],
    )

    target_lore = relationship(
        "RPGLore",
        foreign_keys=[target_lore_id],
    )

    __table_args__ = (
        UniqueConstraint(
            "source_lore_id",
            "target_lore_id",
            name="uq_lore_relation",
        ),
    )