from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_message import RPGMessage
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.rpg_chat import RPGChatMessageCreate, RPGChatMessageResponse
from app.core.security import get_current_user
from app.websockets.manager import manager

router = APIRouter(prefix="/rpg-chat", tags=["RPG Chat"])


# ===============================
# SEND
# ===============================
@router.post("/{rpg_id}", response_model=RPGChatMessageResponse)
async def send_message(
    rpg_id: int,
    message_data: RPGChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
        raise HTTPException(403, "Você não participa deste RPG")

    message = RPGMessage(
        content=message_data.content,
        user_id=current_user.id,
        rpg_id=rpg_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    await manager.broadcast(
        rpg_id,
        "chat",
        {
            "type": "message",
            "data": {
                "id": message.id,
                "content": message.content,
                "user_id": message.user_id,
                "username": current_user.username,
                "created_at": message.created_at.isoformat()
            }
        }
    )

    return message


# ===============================
# LIST (CORRIGIDO)
# ===============================
@router.get("/{rpg_id}")
def list_messages(rpg_id: int, db: Session = Depends(get_db)):
    messages = (
        db.query(RPGMessage, User.username)
        .join(User, User.id == RPGMessage.user_id)
        .filter(RPGMessage.rpg_id == rpg_id)
        .order_by(RPGMessage.created_at.asc())
        .all()
    )

    return [
        {
            "id": m.RPGMessage.id,
            "content": m.RPGMessage.content,
            "user_id": m.RPGMessage.user_id,
            "username": m.username,
            "created_at": m.RPGMessage.created_at,
        }
        for m in messages
    ]


# ===============================
# EDIT
# ===============================
@router.put("/{message_id}")
async def update_message(
    message_id: int,
    message_data: RPGChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    msg = db.query(RPGMessage).filter(RPGMessage.id == message_id).first()

    if not msg:
        raise HTTPException(404, "Mensagem não encontrada")

    if msg.user_id != current_user.id:
        raise HTTPException(403, "Sem permissão")

    msg.content = message_data.content
    db.commit()
    db.refresh(msg)

    await manager.broadcast(
        msg.rpg_id,
        "chat",
        {
            "type": "edit",
            "data": {
                "id": msg.id,
                "content": msg.content,
            }
        }
    )

    return msg


# ===============================
# DELETE
# ===============================
@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    msg = db.query(RPGMessage).filter(RPGMessage.id == message_id).first()

    if not msg:
        raise HTTPException(404, "Mensagem não encontrada")

    if msg.user_id != current_user.id:
        raise HTTPException(403, "Sem permissão")

    rpg_id = msg.rpg_id

    db.delete(msg)
    db.commit()

    await manager.broadcast(
        rpg_id,
        "chat",
        {
            "type": "delete",
            "message_id": message_id
        }
    )

    return {"ok": True}