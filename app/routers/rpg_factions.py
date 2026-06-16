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
from app.models.rpg_timeline import RPGTimeline
from app.models.character import Character
from app.schemas.rpg_faction import (
    RPGFactionCreate,
    RPGFactionUpdate,
    RPGFactionResponse,
)
from sqlalchemy import func

router = APIRouter(
    prefix="/factions",
    tags=["RPG Factions"],
)


@router.get("/rpg/{rpg_id}")
def get_factions(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    factions = (
        db.query(RPGFaction)
        .filter(RPGFaction.rpg_id == rpg_id)
        .order_by(RPGFaction.name.asc())
        .all()
    )

    return [
        {
            "id": faction.id,
            "name": faction.name,
            "description": faction.description,
            "rpg_id": faction.rpg_id,
            "member_count": (
                db.query(func.count(Character.id))
                .filter(
                    Character.faction_id == faction.id
                )
                .scalar()
            ),
        }
        for faction in factions
    ]

@router.get("/{faction_id}")
def get_faction_detail(
    faction_id: int,
    db: Session = Depends(get_db),
):
    faction = (
        db.query(RPGFaction)
        .filter(
            RPGFaction.id == faction_id
        )
        .first()
    )

    if not faction:
        raise HTTPException(
            status_code=404,
            detail="Facção não encontrada",
        )

    members = (
        db.query(Character)
        .filter(
            Character.faction_id == faction.id
        )
        .order_by(
            Character.name.asc()
        )
        .all()
    )

    timeline_events = (
    db.query(RPGTimeline)
    .filter(
        RPGTimeline.factions.any(
            RPGFaction.id == faction.id
        )
    )
    .order_by(
        RPGTimeline.id.asc()
    )
    .all()
    )

    return {
        "id": faction.id,
        "name": faction.name,
        "description": faction.description,
        "rpg_id": faction.rpg_id,
        "members": [
            {
                "id": member.id,
                "name": member.name,
                "history": member.history,
                "image_url": member.image_url,
                "world_lore_id": member.world_lore_id,
                "world_lore": {
                    "id": member.world_lore.id,
                    "title": member.world_lore.title,
                } if member.world_lore else None,
            }
            for member in members
        ],

        "timeline_events": [
    {
        "id": event.id,
        "title": event.title,
        "content": event.content,
        "date_label": event.date_label,
        "lore": {
            "id": event.lore.id,
            "title": event.lore.title,
        } if event.lore else None,
        "category": {
            "id": event.category.id,
            "name": event.category.name,
        } if event.category else None,
        "characters": [
            {
                "id": character.id,
                "name": character.name,
            }
            for character in event.characters
        ],
    }
    for event in timeline_events
],
     
    }

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