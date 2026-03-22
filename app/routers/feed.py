from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional

from app.db.session import get_db
from app.models.rpg import RPG
from app.models.rpg_participant import RPGParticipant
from app.models.rpg_turn import RPGTurn
from app.models.tag import Tag
from app.schemas.feed import FeedResponse, FeedRPG

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/", response_model=FeedResponse)
def get_feed(
    tag: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    # 🔎 Buscar tag (se existir)
    tag_obj = None
    if tag:
        tag_obj = db.query(Tag).filter(Tag.name == tag).first()

    # 🔥 RECENTES
    recent_query = db.query(RPG)

    if tag_obj:
        recent_query = recent_query.join(RPG.tags).filter(Tag.id == tag_obj.id)

    recent_rpgs = (
        recent_query
        .order_by(RPG.id.desc())
        .limit(10)
        .all()
    )

    # 🔥 POPULARES
    popular_query = (
        db.query(
            RPG,
            func.count(RPGParticipant.id).label("participants_count")
        )
        .join(RPGParticipant, RPGParticipant.rpg_id == RPG.id)
        .filter(RPGParticipant.status == "accepted")
        .group_by(RPG.id)
    )

    if tag_obj:
        popular_query = popular_query.join(RPG.tags).filter(Tag.id == tag_obj.id)

    popular_rpgs = (
        popular_query
        .order_by(func.count(RPGParticipant.id).desc())
        .limit(10)
        .all()
    )

    # 🔥 ATIVOS (últimas 24h)
    one_day_ago = datetime.utcnow() - timedelta(days=1)

    active_ids_query = (
        db.query(RPGTurn.rpg_id)
        .filter(RPGTurn.created_at >= one_day_ago)
        .distinct()
    )

    if tag_obj:
        active_ids_query = (
            active_ids_query
            .join(RPG, RPG.id == RPGTurn.rpg_id)
            .join(RPG.tags)
            .filter(Tag.id == tag_obj.id)
        )

    active_rpg_ids = active_ids_query.subquery()

    active_rpgs = (
        db.query(RPG)
        .filter(RPG.id.in_(active_rpg_ids))
        .limit(10)
        .all()
    )

    # 🔧 Função auxiliar
    def build_rpg_response(rpg, participants_count=0, recent_activity=False):
        return FeedRPG(
            id=rpg.id,
            name=rpg.name,
            description=rpg.description,
            participants_count=participants_count,
            recent_activity=recent_activity
        )

    # 🔄 Montar resposta
    recent = [
        build_rpg_response(rpg)
        for rpg in recent_rpgs
    ]

    popular = [
        build_rpg_response(rpg, participants_count=count)
        for rpg, count in popular_rpgs
    ]

    active = [
        build_rpg_response(rpg, recent_activity=True)
        for rpg in active_rpgs
    ]

    return FeedResponse(
        recent=recent,
        active=active,
        popular=popular
    )