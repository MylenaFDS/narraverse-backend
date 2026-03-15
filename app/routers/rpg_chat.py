from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_message import RPGMessage
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.rpg_chat import RPGChatMessageCreate, RPGChatMessageResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/rpg-chat", tags=["RPG Chat"])


@router.post("/{rpg_id}", response_model=RPGChatMessageResponse)
def send_message(
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
            status_code=403,
            detail="Você não participa deste RPG"
        )

    message = RPGMessage(
        content=message_data.content,
        user_id=current_user.id,
        rpg_id=rpg_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@router.get("/{rpg_id}", response_model=list[RPGChatMessageResponse])
def list_messages(
    rpg_id: int,
    db: Session = Depends(get_db)
):

    messages = (
        db.query(RPGMessage)
        .filter(RPGMessage.rpg_id == rpg_id)
        .order_by(RPGMessage.created_at.asc())
        .all()
    )

    return messages