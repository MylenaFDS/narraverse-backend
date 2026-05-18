from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,

    # 🔥 evita conexão morta
    pool_pre_ping=True,

    # 🔥 recicla conexão antiga
    pool_recycle=300,

    # 🔥 evita QueuePool limit exceeded
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,

    # 🔥 melhora estabilidade no Render/Railway/Supabase
    pool_reset_on_return="rollback",
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()