from sqlalchemy.orm import Session
from app.models.character import Character


def create_character(db: Session, user_id: int, rpg_id: int, data):
    character = Character(
        name=data.name,
        description=data.description,
        sheet=data.sheet,
        user_id=user_id,
        rpg_id=rpg_id
    )

    db.add(character)
    db.commit()
    db.refresh(character)

    return character


def list_characters(db: Session, rpg_id: int):
    return db.query(Character).filter(Character.rpg_id == rpg_id).all()