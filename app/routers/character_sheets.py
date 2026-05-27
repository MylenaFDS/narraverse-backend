from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.character import Character
from app.models.character_sheet_value import CharacterSheetValue
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.character_sheet import (
    CharacterSheetValueCreate,
    CharacterSheetValueResponse
)
from app.core.security import get_current_user

router = APIRouter(prefix="/character-sheets", tags=["Character Sheets"])


@router.post("/{character_id}", response_model=CharacterSheetValueResponse)
def upsert_character_sheet(
    character_id: int,
    data: CharacterSheetValueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    character = db.query(Character).filter(Character.id == character_id).first()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")

    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Você só pode editar a ficha dos seus próprios personagens"
        )

    participant = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == character.rpg_id,
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "accepted"
        )
        .first()
    )

    if not participant:
        raise HTTPException(status_code=403, detail="Sem acesso")

    # 🔥 VERIFICA SE JÁ EXISTE
    existing = (
        db.query(CharacterSheetValue)
        .filter(
            CharacterSheetValue.character_id == character_id,
            CharacterSheetValue.field_id == data.field_id
        )
        .first()
    )

    if existing:
        existing.value = data.value
        db.commit()
        db.refresh(existing)
        return existing

    # 🔥 SENÃO CRIA
    new_value = CharacterSheetValue(
        character_id=character_id,
        field_id=data.field_id,
        value=data.value
    )

    db.add(new_value)
    db.commit()
    db.refresh(new_value)

    return new_value

@router.get("/{character_id}", response_model=list[CharacterSheetValueResponse])
def get_character_sheet(
    character_id: int,
    db: Session = Depends(get_db)
):

    sheet = (
        db.query(CharacterSheetValue)
        .filter(CharacterSheetValue.character_id == character_id)
        .all()
    )

    return sheet