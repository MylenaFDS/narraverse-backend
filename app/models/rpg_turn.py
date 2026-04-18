from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Table, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


# tabela intermediária de menções
turn_mentions = Table(
    "turn_mentions",
    Base.metadata,
    Column("turn_id", Integer, ForeignKey("rpg_turns.id")),
    Column("participant_id", Integer, ForeignKey("rpg_participants.id")),
)


class RPGTurn(Base):
    __tablename__ = "rpg_turns"

    id = Column(Integer, primary_key=True, index=True)

    rpg_id = Column(Integer, ForeignKey("rpgs.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)

    reply_to_turn_id = Column(Integer, ForeignKey("rpg_turns.id"), nullable=True, index=True)

    # RELAÇÕES

    rpg = relationship("RPG")

    user = relationship("User")
    
    character = relationship ("Character")
    # relação pai/filho dos turnos
    parent_turn = relationship(
        "RPGTurn",
        remote_side=[id],
        backref="replies"
    )

    # participantes mencionados
    mentioned_participants = relationship(
        "RPGParticipant",
        secondary=turn_mentions
    )

    __table_args__ = (
        Index("idx_turn_rpg_created", "rpg_id", "created_at"),
    )