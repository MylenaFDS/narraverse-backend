from sqlalchemy.orm import Session, joinedload

from app.models.inventory_item import InventoryItem
from app.models.item import Item


def list_inventory(
    db: Session,
    character_id: int,
):
    return (
        db.query(InventoryItem)
        .options(
            joinedload(InventoryItem.item)
        )
        .filter(
            InventoryItem.character_id == character_id
        )
        .all()
    )


def add_item(
    db: Session,
    character_id: int,
    item_id: int,
    quantity: int = 1,
):
    inventory_item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.character_id == character_id,
            InventoryItem.item_id == item_id,
        )
        .first()
    )

    if inventory_item:
        inventory_item.quantity += quantity

    else:
        inventory_item = InventoryItem(
            character_id=character_id,
            item_id=item_id,
            quantity=quantity,
            equipped=False,
        )

        db.add(inventory_item)

    db.commit()
    db.refresh(inventory_item)

    return inventory_item


def remove_item(
    db: Session,
    inventory_item_id: int,
):
    inventory_item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.id == inventory_item_id
        )
        .first()
    )

    if not inventory_item:
        return None

    db.delete(inventory_item)

    db.commit()

    return True


def equip_item(
    db: Session,
    inventory_item_id: int,
):
    inventory_item = (
        db.query(InventoryItem)
        .options(
            joinedload(InventoryItem.item)
        )
        .filter(
            InventoryItem.id == inventory_item_id
        )
        .first()
    )

    if not inventory_item:
        return None

    # Desequipa itens da mesma categoria
    equipped_items = (
        db.query(InventoryItem)
        .join(Item)
        .filter(
            InventoryItem.character_id == inventory_item.character_id,
            InventoryItem.equipped == True,
            Item.category == inventory_item.item.category,
        )
        .all()
    )

    for item in equipped_items:
        item.equipped = False

    inventory_item.equipped = True

    db.commit()
    db.refresh(inventory_item)

    return inventory_item


def unequip_item(
    db: Session,
    inventory_item_id: int,
):
    inventory_item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.id == inventory_item_id
        )
        .first()
    )

    if not inventory_item:
        return None

    inventory_item.equipped = False

    db.commit()
    db.refresh(inventory_item)

    return inventory_item


def use_item(
    db: Session,
    inventory_item_id: int,
):
    inventory_item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.id == inventory_item_id
        )
        .first()
    )

    if not inventory_item:
        return None

    inventory_item.quantity -= 1

    if inventory_item.quantity <= 0:
        db.delete(inventory_item)

    db.commit()

    return True