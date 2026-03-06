from sqlalchemy.orm import Session
from app.models.rpg_turn import RPGTurn
from app.models.rpg_participant import RPGParticipant


def create_turn(db: Session, rpg_id: int, user_id: int, data):

    turn = RPGTurn(
        rpg_id=rpg_id,
        author_id=user_id,
        content=data.content
    )

    if data.mentioned_participants:

        participants = db.query(RPGParticipant).filter(
            RPGParticipant.id.in_(data.mentioned_participants)
        ).all()

        turn.mentioned_participants = participants

    db.add(turn)
    db.commit()
    db.refresh(turn)

    return turn