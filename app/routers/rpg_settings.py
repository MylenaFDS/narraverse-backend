from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.rpg_settings import (
    RPGSettings,
)

from app.schemas.rpg_settings import (
    RPGSettingsUpdate,
    RPGSettingsResponse,
)

router = APIRouter(
    prefix="/rpg-settings",
    tags=["RPG Settings"],
)

@router.get(
    "/{rpg_id}",
    response_model=RPGSettingsResponse,
)
def get_settings(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    settings = (
        db.query(RPGSettings)
        .filter(
            RPGSettings.rpg_id
            == rpg_id
        )
        .first()
    )

    if not settings:
        settings = RPGSettings(
            rpg_id=rpg_id
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings

@router.put(
    "/{rpg_id}",
    response_model=RPGSettingsResponse,
)
def update_settings(
    rpg_id: int,
    data: RPGSettingsUpdate,
    db: Session = Depends(get_db),
):
    settings = (
        db.query(RPGSettings)
        .filter(
            RPGSettings.rpg_id
            == rpg_id
        )
        .first()
    )

    if not settings:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada",
        )

    settings.use_ai_assistant = (
        data.use_ai_assistant
    )

    settings.use_ai_narrator = (
        data.use_ai_narrator
    )

    settings.use_ai_events = (
        data.use_ai_events
    )

    settings.use_ai_npcs = (
        data.use_ai_npcs
    )

    db.commit()
    db.refresh(settings)

    return settings