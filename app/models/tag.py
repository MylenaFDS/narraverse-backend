from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.rpg_tag import rpg_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    rpgs = relationship(
        "RPG",
        secondary=rpg_tags,
        back_populates="tags"
    )