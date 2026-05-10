from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.rpg import RPG
from app.models.map_region import MapRegion
from app.schemas.map_region import (
    MapRegionCreate,
    MapRegionResponse,
)

router = APIRouter(prefix="/rpgs", tags=["Map Regions"])

@router.get("/{rpg_id}/map-regions", response_model=list[MapRegionResponse])
def get_map_regions(rpg_id: int, db: Session = Depends(get_db)):
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    regions = (
        db.query(MapRegion)
        .filter(MapRegion.rpg_id == rpg_id)
        .all()
    )

    return regions

@router.post("/{rpg_id}/map-regions", response_model=MapRegionResponse)
def create_map_region(
    rpg_id: int,
    data: MapRegionCreate,
    db: Session = Depends(get_db),
):
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    region = MapRegion(
        name=data.name,
        lore_id=data.lore_id,

pos_x=data.pos_x,
pos_y=data.pos_y,

color=data.color,
        rpg_id=rpg_id,
    )
    db.add(region)
    db.commit()
    db.refresh(region)
    return region