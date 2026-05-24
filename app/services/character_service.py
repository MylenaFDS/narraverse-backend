from sqlalchemy.orm import Session

from app.models.character import Character
from app.models.character_sheet_value import CharacterSheetValue


def create_character(db: Session, user_id: int, rpg_id: int, data):
    character = Character(
        name=data.name,
        description=data.description,
        history=data.history,
        world_lore_id=data.world_lore_id,
        image_url=data.image_url,
        user_id=user_id,
        rpg_id=rpg_id,
    )

    db.add(character)
    db.commit()
    db.refresh(character)

    if data.sheet:
        for field in data.sheet:
            sheet_value = CharacterSheetValue(
                character_id=character.id,
                field_id=field.field_id,
                value=field.value,
            )
            db.add(sheet_value)

        db.commit()

    return character

def list_characters(db: Session, rpg_id: int):
    return db.query(Character).filter(Character.rpg_id == rpg_id).all()