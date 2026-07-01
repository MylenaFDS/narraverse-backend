from pydantic import BaseModel

from app.schemas.item import ItemResponse


class InventoryItemResponse(BaseModel):

    id: int

    quantity: int

    equipped: bool

    item: ItemResponse

    class Config:
        from_attributes = True