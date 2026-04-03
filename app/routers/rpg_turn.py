from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_turn import RPGTurn
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.rpg_turn import RPGTurnCreate, RPGTurnResponse
from app.core.security import get_current_user
from app.services.notification_service import create_notification

router = APIRouter(prefix="/rpg-turns", tags=["RPG Turns"])


# ===============================
# 🔥 CREATE TURN
# ===============================
@router.post("/{rpg_id}", response_model=RPGTurnResponse)
def create_turn(
    rpg_id: int,
    turn_data: RPGTurnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # verifica participação
    participant = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "accepted",
        )
        .first()
    )

    if not participant:
        raise HTTPException(
            status_code=403,
            detail="Você não participa deste RPG"
        )

    parent_turn = None

    # valida reply
    if turn_data.reply_to_turn_id:
        parent_turn = (
            db.query(RPGTurn)
            .filter(
                RPGTurn.id == turn_data.reply_to_turn_id,
                RPGTurn.rpg_id == rpg_id,
            )
            .first()
        )

        if not parent_turn:
            raise HTTPException(
                status_code=404,
                detail="Turno que você está tentando responder não existe"
            )

    # cria turno
    turn = RPGTurn(
        rpg_id=rpg_id,
        user_id=current_user.id,
        content=turn_data.content,
        reply_to_turn_id=turn_data.reply_to_turn_id,
    )

    # menções
    if turn_data.mentioned_participants:
        participants = (
            db.query(RPGParticipant)
            .filter(
                RPGParticipant.id.in_(turn_data.mentioned_participants),
                RPGParticipant.rpg_id == rpg_id,
            )
            .all()
        )

        turn.mentioned_participants = participants

    db.add(turn)
    db.commit()
    db.refresh(turn)

    # 🔔 notificação reply
    if parent_turn and parent_turn.user_id != current_user.id:
        create_notification(
            db,
            parent_turn.user_id,
            f"{current_user.email} respondeu seu turno."
        )

    # 🔔 notificação menção
    if turn_data.mentioned_participants:
        for participant in turn.mentioned_participants:
            if participant.user_id != current_user.id:
                create_notification(
                    db,
                    participant.user_id,
                    f"{current_user.email} mencionou você em um turno."
                )

    return RPGTurnResponse(
        id=turn.id,
        content=turn.content,
        user_id=turn.user_id,
        created_at=turn.created_at,
        reply_to_turn_id=turn.reply_to_turn_id,
        mentioned_participants=[p.id for p in turn.mentioned_participants],
    )


# ===============================
# 🔥 LIST TURNS
# ===============================
@router.get("/{rpg_id}", response_model=list[RPGTurnResponse])
def list_turns(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    turns = (
        db.query(RPGTurn)
        .filter(RPGTurn.rpg_id == rpg_id)
        .order_by(RPGTurn.created_at.asc())
        .all()
    )

    return [
        RPGTurnResponse(
            id=t.id,
            content=t.content,
            user_id=t.user_id,
            created_at=t.created_at,
            reply_to_turn_id=t.reply_to_turn_id,
            mentioned_participants=[p.id for p in t.mentioned_participants],
        )
        for t in turns
    ]


# ===============================
# 🔥 GET THREAD
# ===============================
@router.get("/{rpg_id}/thread/{turn_id}", response_model=list[RPGTurnResponse])
def get_turn_thread(
    rpg_id: int,
    turn_id: int,
    db: Session = Depends(get_db),
):
    parent = (
        db.query(RPGTurn)
        .filter(
            RPGTurn.id == turn_id,
            RPGTurn.rpg_id == rpg_id,
        )
        .first()
    )

    if not parent:
        raise HTTPException(status_code=404, detail="Turno não encontrado")

    replies = (
        db.query(RPGTurn)
        .filter(RPGTurn.reply_to_turn_id == turn_id)
        .order_by(RPGTurn.created_at.asc())
        .all()
    )

    return [
        RPGTurnResponse(
            id=t.id,
            content=t.content,
            user_id=t.user_id,
            created_at=t.created_at,
            reply_to_turn_id=t.reply_to_turn_id,
            mentioned_participants=[p.id for p in t.mentioned_participants],
        )
        for t in replies
    ]


# ===============================
# 🔥 DELETE TURN
# ===============================
@router.delete("/{turn_id}")
def delete_turn(
    turn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    turn = db.query(RPGTurn).filter(RPGTurn.id == turn_id).first()

    if not turn:
        raise HTTPException(status_code=404, detail="Turno não encontrado")

    # 🔥 segurança: só dono pode deletar
    if turn.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    db.delete(turn)
    db.commit()

    return {"message": "Turno deletado com sucesso"}