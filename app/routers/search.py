from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg import RPG
from app.models.character import Character
from app.models.rpg_lore import RPGLore
from app.schemas.search import SearchResponse, SearchItem

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=SearchResponse)
def global_search(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):

    # 🔎 Buscar RPGs
    rpgs = (
        db.query(RPG)
        .filter(RPG.name.ilike(f"%{q}%"))
        .limit(10)
        .all()
    )

    # 🔎 Buscar personagens
    characters = (
        db.query(Character)
        .filter(Character.name.ilike(f"%{q}%"))
        .limit(10)
        .all()
    )

    # 🔎 Buscar lore (apenas aprovada)
    lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.title.ilike(f"%{q}%"),
            RPGLore.is_approved == True
        )
        .limit(10)
        .all()
    )

    return SearchResponse(
        rpgs=[SearchItem(id=r.id, title=r.name) for r in rpgs],
        characters=[SearchItem(id=c.id, title=c.name) for c in characters],
        lore=[SearchItem(id=l.id, title=l.title) for l in lore],
    )