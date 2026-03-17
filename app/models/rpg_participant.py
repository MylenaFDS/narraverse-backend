from sqlalchemy import Column, Integer, ForeignKey, String, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class RPGParticipant(Base):
    __tablename__ = "rpg_participants"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False, index=True)

    status = Column(String(20), default="pending")
    # invited | pending | accepted | rejected

    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])

    rpg = relationship("RPG", back_populates="participants")

    __table_args__ = (
        Index("idx_participant_user_rpg", "user_id", "rpg_id"),
    )