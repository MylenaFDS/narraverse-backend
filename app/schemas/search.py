from pydantic import BaseModel
from typing import List


class SearchItem(BaseModel):
    id: int
    title: str


class SearchResponse(BaseModel):
    rpgs: List[SearchItem]
    characters: List[SearchItem]
    lore: List[SearchItem]