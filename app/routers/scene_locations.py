from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.region_scene import RegionScene
from app.models.scene_location import SceneLocation

from app.schemas.scene_location import (
    SceneLocationCreate,
    SceneLocationUpdate,
    SceneLocationResponse,
)

router = APIRouter(
    prefix="/scene-locations",
    tags=["Scene Locations"],
)

@router.post(
    "/scene/{scene_id}",
    response_model=SceneLocationResponse,
)
def create_scene_location(
    scene_id: int,
    data: SceneLocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scene = (
        db.query(RegionScene)
        .filter(RegionScene.id == scene_id)
        .first()
    )

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Cena não encontrada",
        )

    location = SceneLocation(
        name=data.name,
        description=data.description,
        pos_x=data.pos_x,
        pos_y=data.pos_y,
        scene_id=scene_id,
        target_scene_id=data.target_scene_id,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location

@router.get(
    "/scene/{scene_id}",
    response_model=list[SceneLocationResponse],
)
def get_scene_locations(
    scene_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(SceneLocation)
        .filter(SceneLocation.scene_id == scene_id)
        .order_by(SceneLocation.id.asc())
        .all()
    )
@router.put(
    "/{location_id}",
    response_model=SceneLocationResponse,
)
def update_scene_location(
    location_id: int,
    data: SceneLocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    location = (
        db.query(SceneLocation)
        .filter(
            SceneLocation.id
            == location_id
        )
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Local não encontrado",
        )

    location.name = data.name
    location.description = data.description
    location.pos_x = data.pos_x
    location.pos_y = data.pos_y
    location.target_scene_id = (
        data.target_scene_id
    )

    db.commit()
    db.refresh(location)

    return location


@router.delete("/{location_id}")
def delete_scene_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    location = (
        db.query(SceneLocation)
        .filter(
            SceneLocation.id == location_id
        )
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Local não encontrado",
        )

    db.delete(location)
    db.commit()

    return {
        "message": "Local removido"
    }