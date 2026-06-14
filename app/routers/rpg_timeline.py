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
from app.models.rpg_timeline_category import (
    RPGTimelineCategory,
)
from app.models.rpg_turn import RPGTurn
from app.models.character import Character
from app.models.rpg_faction import RPGFaction

from app.schemas.rpg_timeline import (
    RPGTimelineCreate,
    RPGTimelineUpdate,
    RPGTimelineResponse,
)


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


def get_valid_characters(
    db: Session,
    rpg_id: int,
    character_ids: list[int],
):
    if not character_ids:
        return []

    characters = (
        db.query(Character)
        .filter(
            Character.id.in_(
                character_ids
            ),
            Character.rpg_id == rpg_id,
        )
        .all()
    )

    if len(characters) != len(character_ids):
        raise HTTPException(
            status_code=404,
            detail="Um ou mais personagens não foram encontrados",
        )

    return characters

def get_valid_factions(
    db: Session,
    rpg_id: int,
    faction_ids: list[int],
):
    if not faction_ids:
        return []

    factions = (
        db.query(RPGFaction)
        .filter(
            RPGFaction.id.in_(
                faction_ids
            ),
            RPGFaction.rpg_id == rpg_id,
        )
        .all()
    )

    if len(factions) != len(faction_ids):
        raise HTTPException(
            status_code=404,
            detail="Uma ou mais facções não foram encontradas",
        )

    return factions

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

    if data.category_id:
        category = (
            db.query(RPGTimelineCategory)
            .filter(
                RPGTimelineCategory.id == data.category_id,
                RPGTimelineCategory.rpg_id == rpg_id,
            )
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada",
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

    characters = get_valid_characters(
        db=db,
        rpg_id=rpg_id,
        character_ids=data.character_ids,
    )
    factions = get_valid_factions(
    db=db,
    rpg_id=rpg_id,
    faction_ids=data.faction_ids,
    )

    event = RPGTimeline(
        title=data.title,
        content=data.content,
        date_label=data.date_label,
        lore_id=data.lore_id,
        turn_id=data.turn_id,
        category_id=data.category_id,
        rpg_id=rpg_id,
        author_id=current_user.id,
    )

    event.characters = characters
    event.factions = factions

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

    if data.category_id:
        category = (
            db.query(
                RPGTimelineCategory
            )
            .filter(
                RPGTimelineCategory.id
                == data.category_id,
                RPGTimelineCategory.rpg_id
                == event.rpg_id,
            )
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada",
            )

    if data.turn_id:
        turn = (
            db.query(RPGTurn)
            .filter(
                RPGTurn.id == data.turn_id,
                RPGTurn.rpg_id == event.rpg_id,
            )
            .first()
        )

        if not turn:
            raise HTTPException(
                status_code=404,
                detail="Turno não encontrado",
            )

    characters = None

    if data.character_ids is not None:
        characters = get_valid_characters(
            db=db,
            rpg_id=event.rpg_id,
            character_ids=data.character_ids,
        )

    factions = None

    if data.faction_ids is not None:
        factions = get_valid_factions(
            db=db,
            rpg_id=event.rpg_id,
            faction_ids=data.faction_ids,
        )

    event.title = data.title
    event.content = data.content
    event.date_label = data.date_label
    event.lore_id = data.lore_id
    event.turn_id = data.turn_id
    event.category_id = data.category_id
    if characters is not None:
        event.characters = characters
    if factions is not None:
        event.factions = factions
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


@router.get(
    "/lore/{lore_id}",
    response_model=list[RPGTimelineResponse],
)
def get_timeline_by_lore(
    lore_id: int,
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

    return (
        db.query(RPGTimeline)
        .filter(
            RPGTimeline.lore_id == lore_id
        )
        .order_by(
            RPGTimeline.id.asc()
        )
        .all()
    )

@router.get(
    "/character/{character_id}",
    response_model=list[RPGTimelineResponse],
)
def get_timeline_by_character(
    character_id: int,
    db: Session = Depends(get_db),
):
    character = (
        db.query(Character)
        .filter(
            Character.id == character_id
        )
        .first()
    )

    if not character:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrado",
        )

    return (
        db.query(RPGTimeline)
        .filter(
            RPGTimeline.characters.any(
                Character.id == character_id
            )
        )
        .order_by(
            RPGTimeline.id.asc()
        )
        .all()
    )