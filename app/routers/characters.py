from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterResponse
from app.core.security import get_current_user
from app.services.character_service import (
    create_character,
    list_characters,
    list_npcs,
)
from app.models.character_sheet_value import CharacterSheetValue
from app.models.rpg_sheet_field import RPGSheetField
from app.models.rpg_turn import RPGTurn
from app.models.rpg_lore import RPGLore
from typing import Optional
import os
import shutil

router = APIRouter(prefix="/characters", tags=["Characters"])

@router.get("/me")
def get_my_characters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    

    return db.query(Character).filter(
        Character.user_id == current_user.id
    ).all()

@router.get("/lore/{lore_id}")
def get_characters_by_lore(
    lore_id: int,
    db: Session = Depends(get_db),
):
    lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.id == lore_id
        )
        .first()
    )

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore não encontrada",
        )

    characters = (
        db.query(Character)
        .filter(
            Character.world_lore_id == lore_id
        )
        .all()
    )

    return [
    {
        "id": character.id,
        "name": character.name,
        "history": character.history,
        "image_url": character.image_url,
        "world_lore_id": character.world_lore_id,
        "faction_id": character.faction_id,
        "faction": {
            "id": character.faction.id,
            "name": character.faction.name,
        } if character.faction else None,
    }
    for character in characters
]

@router.get("/rpg/{rpg_id}/public")
def get_public_characters_by_rpg(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    characters = (
        db.query(Character)
        .filter(
            Character.rpg_id == rpg_id,
            Character.is_npc == False,
        )
        .all()
    )

    return [
        {
            "id": char.id,
            "name": char.name,
            "image_url": char.image_url,
            "user_id": char.user_id,
        }
        for char in characters
    ]

@router.get("/rpg/{rpg_id}/public-npcs")
def get_public_npcs_by_rpg(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    npcs = (
        db.query(Character)
        .filter(
            Character.rpg_id == rpg_id,
            Character.is_npc == True,
        )
        .all()
    )

    return [
        {
            "id": npc.id,
            "name": npc.name,
            "image_url": npc.image_url,
        }
        for npc in npcs
    ]

@router.get("/{character_id}/public")
def get_public_character(
    character_id: int,
    db: Session = Depends(get_db),
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

    sheet_values = (
        db.query(CharacterSheetValue, RPGSheetField)
        .join(
            RPGSheetField,
            RPGSheetField.id == CharacterSheetValue.field_id
        )
        .filter(
            CharacterSheetValue.character_id == character.id
        )
        .all()
    )

    return {
    "id": character.id,
    "name": character.name,
    "history": character.history,
    "image_url": character.image_url,
    "world_lore_id": character.world_lore_id,
    "world_lore": {
        "id": character.world_lore.id,
        "title": character.world_lore.title,
    } if character.world_lore else None,
    "faction_id": character.faction_id,
    "faction": {
        "id": character.faction.id,
        "name": character.faction.name,
    } if character.faction else None,
    "owner_id": character.user_id,
    "owner_username": character.owner.username,
    "sheet": [
        {
            "field_id": field.id,
            "field_name": field.name,
            "field_type": field.field_type,
            "value": value.value,
        }
        for value, field in sheet_values
    ],
}

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


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character_route(
    character_id: int,
    name: str = Form(...),
    history: str = Form(...),
    world_lore_id: Optional[int] = Form(None),
    faction_id: Optional[int] = Form(None),
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
    character.faction_id = faction_id
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

@router.get("/{rpg_id}/npcs", response_model=list[CharacterResponse])
def list_npcs_route(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    return list_npcs(db, rpg_id)

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

    # Remove turnos do personagem
    turns = db.query(RPGTurn).filter(
        RPGTurn.character_id == character.id
    ).all()

    for turn in turns:
        db.delete(turn)

    db.flush()

    # Remove personagem
    db.delete(character)

    db.commit()
    return {
        "message": "Personagem excluído com sucesso"
    }

