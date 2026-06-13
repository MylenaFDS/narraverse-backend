from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.rpg import RPG
from app.models.rpg_faction import RPGFaction

from app.schemas.rpg_faction import (
    RPGFactionCreate,
    RPGFactionUpdate,
    RPGFactionResponse,
)


router = APIRouter(
    prefix="/factions",
    tags=["RPG Factions"],
)


@router.get(
    "/rpg/{rpg_id}",
    response_model=list[RPGFactionResponse],
)
def get_factions(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RPGFaction)
        .filter(
            RPGFaction.rpg_id == rpg_id
        )
        .order_by(
            RPGFaction.name.asc()
        )
        .all()
    )


@router.post(
    "/rpg/{rpg_id}",
    response_model=RPGFactionResponse,
)
def create_faction(
    rpg_id: int,
    data: RPGFactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado",
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o mestre pode criar facções",
        )

    faction = RPGFaction(
        name=data.name,
        description=data.description,
        rpg_id=rpg_id,
    )

    db.add(faction)
    db.commit()
    db.refresh(faction)

    return faction


@router.put(
    "/{faction_id}",
    response_model=RPGFactionResponse,
)
def update_faction(
    faction_id: int,
    data: RPGFactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    faction = (
        db.query(RPGFaction)
        .filter(RPGFaction.id == faction_id)
        .first()
    )

    if not faction:
        raise HTTPException(
            status_code=404,
            detail="Facção não encontrada",
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == faction.rpg_id)
        .first()
    )

    if (
        not rpg
        or rpg.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Sem permissão",
        )

    faction.name = data.name
    faction.description = data.description

    db.commit()
    db.refresh(faction)

    return faction


@router.delete("/{faction_id}")
def delete_faction(
    faction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    faction = (
        db.query(RPGFaction)
        .filter(RPGFaction.id == faction_id)
        .first()
    )

    if not faction:
        raise HTTPException(
            status_code=404,
            detail="Facção não encontrada",
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == faction.rpg_id)
        .first()
    )

    if (
        not rpg
        or rpg.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Sem permissão",
        )

    db.delete(faction)
    db.commit()

    return {
        "message": "Facção removida"
    }