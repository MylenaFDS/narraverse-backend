from sqlalchemy import String, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    bio = Column(Text, nullable=True)

    posts = relationship("Post", back_populates="owner")

    # 🔥 RELAÇÃO CORRETA
    owned_rpgs = relationship("RPG", back_populates="owner")