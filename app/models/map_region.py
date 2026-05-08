# Model (`app/models/map_region.py`)


from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class MapRegion(Base):
    __tablename__ = "map_regions"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    rpg_id = Column(Integer, ForeignKey("rpgs.id", ondelete="CASCADE"))

    rpg = relationship("RPG", back_populates="map_regions")
