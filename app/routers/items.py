from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.item import (
    ItemCreate,
    ItemResponse,
)

from app.services.item_service import (
    list_items,
    get_item,
    create_item,
    update_item,
    delete_item,
)

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.get(
    "",
    response_model=list[ItemResponse],
)
def get_all_items(
    db: Session = Depends(get_db),
):
    return list_items(db)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
def get_single_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = get_item(
        db,
        item_id,
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return item


@router.post(
    "",
    response_model=ItemResponse,
)
def create_new_item(
    data: ItemCreate,
    db: Session = Depends(get_db),
):
    return create_item(
        db,
        data,
    )


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
)
def update_existing_item(
    item_id: int,
    data: ItemCreate,
    db: Session = Depends(get_db),
):
    item = update_item(
        db,
        item_id,
        data,
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return item


@router.delete(
    "/{item_id}",
)
def delete_existing_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    success = delete_item(
        db,
        item_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado",
        )

    return {
        "message": "Item removido",
    }