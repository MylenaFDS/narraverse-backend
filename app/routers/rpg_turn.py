from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_turn import RPGTurn
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.rpg_turn import RPGTurnCreate, RPGTurnResponse
from app.core.security import get_current_user
from app.services.notification_service import create_notification
from app.websockets.manager import manager

router = APIRouter(prefix="/rpg-turns", tags=["RPG Turns"])


@router.post("/{rpg_id}", response_model=RPGTurnResponse)
async def create_turn(
    rpg_id: int,
    turn_data: RPGTurnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    from app.models.character import Character

    # ===============================
    # VERIFICA PARTICIPAÇÃO
    # ===============================
    participant = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "accepted"
        )
        .first()
    )

    if not participant:
        raise HTTPException(
            status_code=403,
            detail="Você não participa deste RPG"
        )

    # ===============================
    # BUSCAR PERSONAGEM AUTOR
    # ===============================
    author_character = None

    if turn_data.character_id:
        author_character = db.query(Character).filter(
            Character.id == turn_data.character_id
        ).first()

        if not author_character:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")

        if author_character.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Esse personagem não é seu")

    # ===============================
    # VALIDAR RESPOSTA
    # ===============================
    parent_turn = None

    if turn_data.reply_to_turn_id:
        parent_turn = (
            db.query(RPGTurn)
            .filter(
                RPGTurn.id == turn_data.reply_to_turn_id,
                RPGTurn.rpg_id == rpg_id
            )
            .first()
        )

        if not parent_turn:
            raise HTTPException(
                status_code=404,
                detail="Turno que você está tentando responder não existe"
            )

    # ===============================
    # CRIAR TURNO
    # ===============================
    turn = RPGTurn(
        rpg_id=rpg_id,
        user_id=current_user.id,
        content=turn_data.content,
        reply_to_turn_id=turn_data.reply_to_turn_id,
        character_id=turn_data.character_id,
        mentioned_characters=turn_data.mentioned_characters or []
    )

    # ===============================
    # MENÇÕES (LEGADO)
    # ===============================
    if turn_data.mentioned_participants:
        participants = (
            db.query(RPGParticipant)
            .filter(
                RPGParticipant.id.in_(turn_data.mentioned_participants),
                RPGParticipant.rpg_id == rpg_id
            )
            .all()
        )

        turn.mentioned_participants = participants

    db.add(turn)
    db.commit()
    db.refresh(turn)

    # ===============================
    # 🔥 WEBSOCKET
    # ===============================
    await manager.broadcast(rpg_id, {
        "type": "new_turn",
        "data": {
            "id": turn.id,
            "content": turn.content,
            "user_id": turn.user_id,
            "created_at": str(turn.created_at),
            "reply_to_turn_id": turn.reply_to_turn_id,
            "mentioned_participants": [p.id for p in turn.mentioned_participants],
            "mentioned_characters": turn.mentioned_characters or [],
            "character_id": turn.character_id
        }
    })

    # ===============================
    # 🔔 NOTIFICAÇÕES
    # ===============================
    actor_name = (
        author_character.name if author_character else current_user.email
    )

    notified_users = set()

    # 🔔 RESPOSTA
    if parent_turn and parent_turn.user_id != current_user.id:
        create_notification(
            db,
            parent_turn.user_id,
            f"{actor_name} respondeu seu turno."
        )
        notified_users.add(parent_turn.user_id)

    # 🔔 MENÇÕES (LEGADO)
    if turn.mentioned_participants:
        for participant in turn.mentioned_participants:
            if (
                participant.user_id != current_user.id
                and participant.user_id not in notified_users
            ):
                create_notification(
                    db,
                    participant.user_id,
                    f"{actor_name} mencionou você em um turno."
                )
                notified_users.add(participant.user_id)

    # 🔔 MENÇÕES (PERSONAGENS - OTIMIZADO)
    if turn.mentioned_characters:
        characters = (
            db.query(Character)
            .filter(Character.id.in_(turn.mentioned_characters))
            .all()
        )

        for char in characters:
            if (
                char.user_id != current_user.id
                and char.user_id not in notified_users
            ):
                create_notification(
                    db,
                    char.user_id,
                    f"{actor_name} mencionou {char.name}."
                )
                notified_users.add(char.user_id)

    # ===============================
    # RESPONSE
    # ===============================
    return RPGTurnResponse(
        id=turn.id,
        content=turn.content,
        user_id=turn.user_id,
        created_at=turn.created_at,
        reply_to_turn_id=turn.reply_to_turn_id,
        mentioned_participants=[p.id for p in turn.mentioned_participants],
        mentioned_characters=turn.mentioned_characters or [],
        character_id=turn.character_id
    )

@router.get("/{rpg_id}", response_model=list[RPGTurnResponse])
def list_turns(
    rpg_id: int,
    db: Session = Depends(get_db)
):

    turns = (
        db.query(RPGTurn)
        .filter(RPGTurn.rpg_id == rpg_id)
        .order_by(RPGTurn.created_at.asc())
        .all()
    )

    result = []

    for turn in turns:
        result.append(
            RPGTurnResponse(
                id=turn.id,
                content=turn.content,
                user_id=turn.user_id,
                created_at=turn.created_at,
                reply_to_turn_id=turn.reply_to_turn_id,
                mentioned_participants=[p.id for p in turn.mentioned_participants],
                mentioned_characters=turn.mentioned_characters or [],
                character_id=turn.character_id
            )
        )

    return result


@router.get("/{rpg_id}/thread/{turn_id}", response_model=list[RPGTurnResponse])
def get_turn_thread(
    rpg_id: int,
    turn_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna todos os turnos que respondem um turno específico
    """

    parent = (
        db.query(RPGTurn)
        .filter(
            RPGTurn.id == turn_id,
            RPGTurn.rpg_id == rpg_id
        )
        .first()
    )

    if not parent:
        raise HTTPException(
            status_code=404,
            detail="Turno não encontrado"
        )

    replies = (
        db.query(RPGTurn)
        .filter(
            RPGTurn.reply_to_turn_id == turn_id
        )
        .order_by(RPGTurn.created_at.asc())
        .all()
    )

    result = []

    for turn in replies:
        result.append(
            RPGTurnResponse(
                id=turn.id,
                content=turn.content,
                user_id=turn.user_id,
                created_at=turn.created_at,
                reply_to_turn_id=turn.reply_to_turn_id,
                mentioned_participants=[p.id for p in turn.mentioned_participants],
                character_id=turn.character_id
            )
        )

    return result

@router.delete("/{turn_id}")
def delete_turn(
    turn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    turn = db.query(RPGTurn).filter(RPGTurn.id == turn_id).first()

    if not turn:
        raise HTTPException(status_code=404, detail="Turno não encontrado")

    if turn.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    # 🔥 DELETE DIRETO (resolve seu problema)
    db.query(RPGTurn).filter(RPGTurn.id == turn_id).delete()
    db.commit()

    return {"message": "Turno deletado com sucesso"}