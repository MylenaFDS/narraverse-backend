from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.character import Character
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.character import CharacterCreate, CharacterResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.post("/{rpg_id}", response_model=CharacterResponse)
def create_character(
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
            RPGParticipant.status == "accepted",
        )
        .first()
    )

    if not participant:
        raise HTTPException(
            status_code=403,
            detail="Você não participa deste RPG"
        )

    character = Character(
        name=character_data.name,
        description=character_data.description,
        sheet=character_data.sheet,
        user_id=current_user.id,
        rpg_id=rpg_id,
    )

    db.add(character)
    db.commit()
    db.refresh(character)

    return character


@router.get("/{rpg_id}", response_model=list[CharacterResponse])
def list_characters(
    rpg_id: int,
    db: Session = Depends(get_db)
):

    characters = (
        db.query(Character)
        .filter(Character.rpg_id == rpg_id)
        .all()
    )

    return characters