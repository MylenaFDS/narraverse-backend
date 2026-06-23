from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
)

from app.db.base import Base


class RPGSettings(Base):
    __tablename__ = "rpg_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    rpg_id = Column(
        Integer,
        ForeignKey("rpgs.id"),
        unique=True,
        nullable=False,
    )

    use_ai_assistant = Column(
        Boolean,
        default=True,
    )

    use_ai_narrator = Column(
        Boolean,
        default=False,
    )

    use_ai_events = Column(
        Boolean,
        default=False,
    )

    use_ai_npcs = Column(
        Boolean,
        default=False,
    )