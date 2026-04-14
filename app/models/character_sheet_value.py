from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class CharacterSheetValue(Base):
    __tablename__ = "character_sheet_values"

    id = Column(Integer, primary_key=True, index=True)

    character_id = Column(Integer, ForeignKey("characters.id"))
    field_id = Column(Integer, ForeignKey("rpg_sheet_fields.id"))

    value = Column(String, nullable=False)

    character = relationship("Character", back_populates="sheet_values")
    field = relationship("RPGSheetField")