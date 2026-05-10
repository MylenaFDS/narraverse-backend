from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class MapRegion(Base):
    __tablename__ = "rpg_map_regions"

    id = Column(Integer, primary_key=True, index=True)

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        nullable=False
    )

    lore_id = Column(
        Integer,
        ForeignKey("rpg_lore.id"),
        nullable=True
    )

    name = Column(String(100), nullable=False)

    # posição no mapa
    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)

    color = Column(String(20), default="#7c3aed")

    # RELATIONSHIPS
    rpg = relationship(
    "RPG",
    back_populates="map_regions"
)
    lore = relationship("RPGLore")