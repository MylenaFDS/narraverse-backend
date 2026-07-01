from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inventory import InventoryItemResponse

from app.services.inventory_service import (
    list_inventory,
    add_item,
    remove_item,
    equip_item,
    unequip_item,
    use_item,
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)

@router.get(
    "/{character_id}",
    response_model=list[InventoryItemResponse],
)
def get_inventory(
    character_id: int,
    db: Session = Depends(get_db),
):
    return list_inventory(
        db,
        character_id,
    )


@router.post(
    "/{character_id}/add/{item_id}",
    response_model=InventoryItemResponse,
)
def add_inventory_item(
    character_id: int,
    item_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
):
    return add_item(
        db,
        character_id,
        item_id,
        quantity,
    )


@router.delete(
    "/item/{inventory_item_id}",
)
def delete_inventory_item(
    inventory_item_id: int,
    db: Session = Depends(get_db),
):
    success = remove_item(
        db,
        inventory_item_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return {
        "message": "Item removido"
    }


@router.post(
    "/equip/{inventory_item_id}",
    response_model=InventoryItemResponse,
)
def equip_inventory_item(
    inventory_item_id: int,
    db: Session = Depends(get_db),
):
    item = equip_item(
        db,
        inventory_item_id,
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return item


@router.post(
    "/unequip/{inventory_item_id}",
    response_model=InventoryItemResponse,
)
def unequip_inventory_item(
    inventory_item_id: int,
    db: Session = Depends(get_db),
):
    item = unequip_item(
        db,
        inventory_item_id,
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return item


@router.post(
    "/use/{inventory_item_id}",
)
def use_inventory_item(
    inventory_item_id: int,
    db: Session = Depends(get_db),
):
    success = use_item(
        db,
        inventory_item_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return {
        "message": "Item utilizado"
    }