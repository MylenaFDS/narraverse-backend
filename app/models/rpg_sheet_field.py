from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class RPGSheetField(Base):
    __tablename__ = "rpg_sheet_fields"

    id = Column(Integer, primary_key=True, index=True)

    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False)

    name = Column(String(100), nullable=False)
    field_type = Column(String(50), default="text")

    category = Column(String, nullable=True)

    rpg = relationship("RPG")