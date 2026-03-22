from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), unique=True, nullable=False, index=True)