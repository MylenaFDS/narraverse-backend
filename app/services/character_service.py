from sqlalchemy.orm import Session, joinedload

from app.models.character import Character
from app.models.character_sheet_value import CharacterSheetValue


def create_character(
    db: Session,
    user_id: int,
    rpg_id: int,
    data,
):
    character = Character(
        name=data.name,
        description=data.description,
        history=data.history,
        world_lore_id=data.world_lore_id,
        faction_id=data.faction_id,
        image_url=data.image_url,
        user_id=user_id,
        rpg_id=rpg_id,
        is_npc=data.is_npc,
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

    db.refresh(character)

    character = (
        db.query(Character)
        .options(
            joinedload(Character.faction),
            joinedload(Character.world_lore),
            joinedload(Character.sheet_values)
            .joinedload(CharacterSheetValue.field),
        )
        .filter(Character.id == character.id)
        .first()
    )

    return character


def list_characters(
    db: Session,
    rpg_id: int,
):
    return (
        db.query(Character)
        .options(
            joinedload(Character.faction),
            joinedload(Character.world_lore),
            joinedload(Character.sheet_values).joinedload(
                CharacterSheetValue.field
            ),
        )
        .filter(
            Character.rpg_id == rpg_id,
            Character.is_npc.is_(False),
        )
        .all()
    )


def list_npcs(
    db: Session,
    rpg_id: int,
):
    return (
        db.query(Character)
        .options(
            joinedload(Character.faction),
            joinedload(Character.world_lore),
            joinedload(Character.sheet_values).joinedload(
                CharacterSheetValue.field
            ),
        )
        .filter(
            Character.rpg_id == rpg_id,
            Character.is_npc.is_(True),
        )
        .all()
    )