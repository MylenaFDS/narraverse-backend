from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.deps import get_db

from app.models.rpg import RPG
from app.models.map_region import MapRegion
from app.models.user import User

from app.schemas.map_region import (
    MapRegionCreate,
    MapRegionResponse,
)

from app.core.security import get_current_user

router = APIRouter(
    prefix="/rpgs",
    tags=["Map Regions"]
)


# ===============================
# 📍 UPDATE POSITION SCHEMA
# ===============================
class UpdateRegionPosition(BaseModel):
    pos_x: int
    pos_y: int


# ===============================
# 🗺️ GET REGIONS
# ===============================
@router.get(
    "/{rpg_id}/map-regions",
    response_model=list[MapRegionResponse]
)
def get_map_regions(
    rpg_id: int,
    db: Session = Depends(get_db)
):
    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    regions = (
        db.query(MapRegion)
        .filter(MapRegion.rpg_id == rpg_id)
        .all()
    )

    return regions


# ===============================
# ➕ CREATE REGION
# ===============================
@router.post(
    "/{rpg_id}/map-regions",
    response_model=MapRegionResponse
)
def create_map_region(
    rpg_id: int,
    data: MapRegionCreate,
    db: Session = Depends(get_db),
):
    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

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


# ===============================
# ✏️ UPDATE REGION POSITION
# ===============================
@router.put(
    "/map-regions/{region_id}/position",
    response_model=MapRegionResponse
)
def update_region_position(
    region_id: int,
    data: UpdateRegionPosition,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    region = (
        db.query(MapRegion)
        .filter(MapRegion.id == region_id)
        .first()
    )

    if not region:
        raise HTTPException(
            status_code=404,
            detail="Região não encontrada"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == region.rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode mover regiões"
        )

    region.pos_x = data.pos_x
    region.pos_y = data.pos_y

    db.commit()
    db.refresh(region)

    return region