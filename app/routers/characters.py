from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.character import CharacterCreate, CharacterResponse
from app.core.security import get_current_user
from app.services.character_service import create_character, list_characters

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.post("/{rpg_id}", response_model=CharacterResponse)
def create_character_route(
    rpg_id: int,
    character_data: CharacterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

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

    return create_character(db, current_user.id, rpg_id, character_data)

@router.get("/me")
def get_my_characters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.character import Character

    return db.query(Character).filter(
        Character.user_id == current_user.id
    ).all()
@router.get("/{rpg_id}", response_model=list[CharacterResponse])
def list_characters_route(
    rpg_id: int,
    db: Session = Depends(get_db)
):
    return list_characters(db, rpg_id)

