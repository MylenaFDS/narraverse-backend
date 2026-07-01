from sqlalchemy.orm import Session

from app.models.item import Item


def list_items(db: Session):
    return db.query(Item).all()


def get_item(db: Session, item_id: int):
    return (
        db.query(Item)
        .filter(Item.id == item_id)
        .first()
    )


def create_item(db: Session, data):
    item = Item(
        name=data.name,
        description=data.description,
        category=data.category,
        rarity=data.rarity,
        weight=data.weight,
        value=data.value,
        modifiers=data.modifiers,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def update_item(
    db: Session,
    item_id: int,
    data,
):
    item = get_item(db, item_id)

    if not item:
        return None

    item.name = data.name
    item.description = data.description
    item.category = data.category
    item.rarity = data.rarity
    item.weight = data.weight
    item.value = data.value
    item.modifiers = data.modifiers

    db.commit()
    db.refresh(item)

    return item


def delete_item(
    db: Session,
    item_id: int,
):
    item = get_item(db, item_id)

    if not item:
        return None

    db.delete(item)
    db.commit()

    return True