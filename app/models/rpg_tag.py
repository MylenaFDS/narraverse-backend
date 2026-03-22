from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

rpg_tags = Table(
    "rpg_tags",
    Base.metadata,
    Column("rpg_id", Integer, ForeignKey("rpgs.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)