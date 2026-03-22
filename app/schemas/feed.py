from pydantic import BaseModel
from typing import List


class FeedRPG(BaseModel):
    id: int
    name: str
    description: str | None
    participants_count: int
    recent_activity: bool

    class Config:
        from_attributes = True


class FeedResponse(BaseModel):
    recent: List[FeedRPG]
    active: List[FeedRPG]
    popular: List[FeedRPG]