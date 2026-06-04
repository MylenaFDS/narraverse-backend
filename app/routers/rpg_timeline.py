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
from app.models.rpg_timeline import RPGTimeline
from app.models.rpg_lore import RPGLore

from app.schemas.rpg_timeline import (
    RPGTimelineCreate,
    RPGTimelineUpdate,
    RPGTimelineResponse,
)
from app.models.rpg_turn import RPGTurn

router = APIRouter(
    prefix="/timeline",
    tags=["RPG Timeline"],
)


@router.get(
    "/rpg/{rpg_id}",
    response_model=list[RPGTimelineResponse],
)
def get_timeline(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RPGTimeline)
        .filter(
            RPGTimeline.rpg_id == rpg_id
        )
        .order_by(
            RPGTimeline.id.asc()
        )
        .all()
    )


@router.post(
    "/rpg/{rpg_id}",
    response_model=RPGTimelineResponse,
)
def create_event(
    rpg_id: int,
    data: RPGTimelineCreate,
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
            detail="Apenas o mestre pode criar eventos",
        )
    if data.lore_id:
        lore = (
            db.query(RPGLore)
            .filter(
                RPGLore.id == data.lore_id,
                RPGLore.rpg_id == rpg_id,
                RPGLore.category == "Mundo",
            )
            .first()
        )
        if not lore:
            raise HTTPException(
                status_code=404,
                detail="Região relacionada não encontrada",
            )
        
    if data.turn_id:
        turn = (
        db.query(RPGTurn)
        .filter(
            RPGTurn.id == data.turn_id,
            RPGTurn.rpg_id == rpg_id,
        )
        .first()
    )

    if not turn:
        raise HTTPException(
            status_code=404,
            detail="Turno não encontrado",
        )
    
    event = RPGTimeline(
    title=data.title,
    content=data.content,
    date_label=data.date_label,
    lore_id=data.lore_id,
    turn_id=data.turn_id,
    rpg_id=rpg_id,
    author_id=current_user.id,
)
    db.add(event)
    db.commit()
    db.refresh(event)

    return event

@router.put(
    "/{event_id}",
    response_model=RPGTimelineResponse,
)
def update_event(
    event_id: int,
    data: RPGTimelineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = (
        db.query(RPGTimeline)
        .filter(
            RPGTimeline.id == event_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado",
        )

    rpg = (
        db.query(RPG)
        .filter(
            RPG.id == event.rpg_id
        )
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

    if data.lore_id:
        lore = (
            db.query(RPGLore)
            .filter(
                RPGLore.id == data.lore_id,
                RPGLore.rpg_id == event.rpg_id,
                RPGLore.category == "Mundo",
            )
            .first()
        )

        if not lore:
            raise HTTPException(
                status_code=404,
                detail="Região relacionada não encontrada",
            )
    event.title = data.title
    event.content = data.content
    event.date_label = data.date_label
    event.lore_id = data.lore_id
    event.turn_id = data.turn_id

    db.commit()
    db.refresh(event)

    return event

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = (
        db.query(RPGTimeline)
        .filter(
            RPGTimeline.id == event_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado",
        )

    rpg = (
        db.query(RPG)
        .filter(
            RPG.id == event.rpg_id
        )
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

    db.delete(event)
    db.commit()

    return {
        "message": "Evento removido"
    }