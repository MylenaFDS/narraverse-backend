from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_message import RPGMessage
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.rpg_chat import RPGChatMessageCreate, RPGChatMessageResponse
from app.core.security import get_current_user
from app.websockets.manager import manager
from datetime import datetime, UTC

router = APIRouter(prefix="/rpg-chat", tags=["RPG Chat"])

# ===============================
# SEND
# ===============================
@router.post(
    "/{rpg_id}",
    response_model=RPGChatMessageResponse
)
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
        raise HTTPException(
            403,
            "Você não participa deste RPG"
        )

    message = RPGMessage(
        content=message_data.content,
        user_id=current_user.id,
        rpg_id=rpg_id,
        reply_to_message_id=
            message_data.reply_to_message_id,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    # 🔥 monta reply completo
    reply_to = None

    if message.reply_to_message_id:
        replied = (
            db.query(
                RPGMessage,
                User.username
            )
            .join(
                User,
                User.id == RPGMessage.user_id
            )
            .filter(
                RPGMessage.id
                == message.reply_to_message_id
            )
            .first()
        )

        if replied:
            reply_to = {
                "id":
                    replied.RPGMessage.id,
                "content":
                    replied.RPGMessage.content,
                "username":
                    replied.username,
            }

    # 🔥 broadcast já com reply
    await manager.broadcast(
        rpg_id,
        "chat",
        {
            "type": "message",
            "data": {
                "id": message.id,
                "content": message.content,
                "user_id": message.user_id,
                "username":
                    current_user.username,
                "created_at":
                    message.created_at.isoformat(),
                "is_edited": False,

                "reply_to_message_id":
                    message.reply_to_message_id,

                "reply_to":
                    reply_to,
            }
        }
    )

    return {
        "id": message.id,
        "content": message.content,
        "user_id": message.user_id,
        "rpg_id": message.rpg_id,
        "created_at":
            message.created_at,
            "is_edited": False,
        "username":
            current_user.username,
        "reply_to_message_id":
            message.reply_to_message_id,
        "reply_to":
            reply_to,
    }



# ===============================
# LIST
# ===============================
@router.get("/{rpg_id}")
def list_messages(
    rpg_id: int,
    db: Session = Depends(get_db)
):
    messages = (
        db.query(
            RPGMessage,
            User.username
        )
        .join(
            User,
            User.id == RPGMessage.user_id
        )
        .filter(
            RPGMessage.rpg_id == rpg_id
        )
        .order_by(
            RPGMessage.created_at.asc()
        )
        .all()
    )

    result = []

    for row in messages:
        msg = row.RPGMessage

        reply_to = None

        if msg.reply_to_message_id:
            replied = (
                db.query(
                    RPGMessage,
                    User.username
                )
                .join(
                    User,
                    User.id == RPGMessage.user_id
                )
                .filter(
                    RPGMessage.id
                    == msg.reply_to_message_id
                )
                .first()
            )

            if replied:
                reply_to = {
                    "id":
                        replied.RPGMessage.id,
                    "content":
                        replied.RPGMessage.content,
                    "username":
                        replied.username,
                }

        result.append({
            "id": msg.id,
            "content": msg.content,
            "user_id": msg.user_id,
            "username": row.username,
            "rpg_id": msg.rpg_id,
            "created_at": msg.created_at,
            "is_edited":
            msg.updated_at is not None
            and msg.updated_at != msg.created_at,
            "reply_to_message_id":
                msg.reply_to_message_id,
            "reply_to":
                reply_to,
        })

    return result
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
    msg.updated_at = datetime.now(UTC)
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
    "is_edited": True,
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