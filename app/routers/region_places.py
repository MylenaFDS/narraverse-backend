from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.rpg_lore import RPGLore
from app.models.region_place import (
    RegionPlace,
)

from app.schemas.region_place import (
    RegionPlaceCreate,
    RegionPlaceResponse,
)

router = APIRouter(
    prefix="/region-places",
    tags=["Region Places"],
)

@router.get(
    "/lore/{lore_id}",
    response_model=list[
        RegionPlaceResponse
    ],
)
def get_region_places(
    lore_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RegionPlace)
        .filter(
            RegionPlace.lore_id == lore_id
        )
        .order_by(
            RegionPlace.name.asc()
        )
        .all()
    )

@router.post(
    "/lore/{lore_id}",
    response_model=RegionPlaceResponse,
)
def create_region_place(
    lore_id: int,
    data: RegionPlaceCreate,
    db: Session = Depends(get_db),
):
    lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.id == lore_id
        )
        .first()
    )

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore não encontrada",
        )

    place = RegionPlace(
        name=data.name,
        description=data.description,
        lore_id=lore_id,
    )

    db.add(place)
    db.commit()
    db.refresh(place)

    return place