from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterResponse
from app.core.security import get_current_user
from app.services.character_service import create_character, list_characters
from app.models.character_sheet_value import CharacterSheetValue
from typing import Optional
import os
import shutil

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

@router.put("/{character_id}", response_model=CharacterResponse)
def update_character_route(
    character_id: int,
    name: str = Form(...),
    history: str = Form(...),
    world_lore_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    character = (
        db.query(Character)
        .filter(Character.id == character_id)
        .first()
    )

    if not character:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrado"
        )

    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Sem permissão"
        )

    character.name = name
    character.history = history
    character.world_lore_id = world_lore_id

    if image:
        upload_dir = "uploads/characters"
        os.makedirs(upload_dir, exist_ok=True)

        filename = f"character_{character_id}_{image.filename}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        character.image_url = file_path.replace("\\", "/")

    db.commit()
    db.refresh(character)

    return character

@router.get("/{rpg_id}", response_model=list[CharacterResponse])
def list_characters_route(
    rpg_id: int,
    db: Session = Depends(get_db)
):
    return list_characters(db, rpg_id)

@router.post("/{character_id}/image")
def upload_character_image(
    character_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    character = (
        db.query(Character)
        .filter(Character.id == character_id)
        .first()
    )

    if not character:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrado"
        )

    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Sem permissão"
        )

    upload_dir = "uploads/characters"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"character_{character_id}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    character.image_url = file_path.replace("\\", "/")

    db.commit()
    db.refresh(character)

    return character

@router.delete("/{character_id}")
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    character = (
        db.query(Character)
        .filter(Character.id == character_id)
        .first()
    )

    if not character:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrado"
        )

    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Sem permissão"
        )

    # Remove valores da ficha
    db.query(CharacterSheetValue).filter(
        CharacterSheetValue.character_id == character.id
    ).delete()

    db.delete(character)
    db.commit()

    return {
        "message": "Personagem excluído com sucesso"
    }
