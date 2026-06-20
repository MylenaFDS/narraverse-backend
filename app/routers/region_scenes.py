from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)

import os
import shutil

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.rpg_lore import RPGLore
from app.models.region_scene import RegionScene

from app.schemas.region_scene import (
    RegionSceneCreate,
    RegionSceneUpdate,
    RegionSceneResponse,
)

router = APIRouter(
    prefix="/region-scenes",
    tags=["Region Scenes"],
)

@router.post(
    "/lore/{lore_id}",
    response_model=RegionSceneResponse,
)
def create_region_scene(
    lore_id: int,
    data: RegionSceneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
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

    scene = RegionScene(
        title=data.title,
        description=data.description,
        lore_id=lore_id,
    )

    db.add(scene)
    db.commit()
    db.refresh(scene)

    return scene

@router.get(
    "/{scene_id}",
    response_model=RegionSceneResponse,
)
def get_region_scene_detail(
    scene_id: int,
    db: Session = Depends(get_db),
):
    scene = (
        db.query(RegionScene)
        .filter(
            RegionScene.id == scene_id
        )
        .first()
    )

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Cena não encontrada",
        )

    return scene

@router.get(
    "/lore/{lore_id}",
    response_model=list[
        RegionSceneResponse
    ],
)
def get_region_scenes(
    lore_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RegionScene)
        .filter(
            RegionScene.lore_id
            == lore_id
        )
        .order_by(
            RegionScene.id.asc()
        )
        .all()
    )

@router.post(
    "/{scene_id}/image",
    response_model=RegionSceneResponse,
)
def upload_region_scene_image(
    scene_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    scene = (
        db.query(RegionScene)
        .filter(
            RegionScene.id == scene_id
        )
        .first()
    )

    if not scene:
        raise HTTPException(
            status_code=404,
            detail="Cena não encontrada",
        )

    upload_dir = "uploads/region_scenes"
    os.makedirs(upload_dir, exist_ok=True)

    if scene.image_url:
        old_path = scene.image_url

        if os.path.exists(old_path):
            os.remove(old_path)

    filename = f"scene_{scene_id}_{file.filename}"
    file_path = os.path.join(
        upload_dir,
        filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    scene.image_url = file_path.replace(
        "\\",
        "/",
    )
    scene.is_ai_generated = False

    db.commit()
    db.refresh(scene)

    return scene