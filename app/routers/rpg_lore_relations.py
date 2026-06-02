from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.rpg_lore import RPGLore
from app.models.rpg_lore_relation import (
    RPGLoreRelation,
)

from app.schemas.rpg_lore_relation import (
    LoreRelationCreate,
    LoreRelationDetailResponse,
)

router = APIRouter(
    prefix="/lore-relations",
    tags=["Lore Relations"],
)

@router.post(
    "/{source_lore_id}",
    response_model=LoreRelationDetailResponse,
)
def create_relation(
    source_lore_id: int,
    data: LoreRelationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    source_lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.id == source_lore_id
        )
        .first()
    )

    target_lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.id == data.target_lore_id
        )
        .first()
    )

    if not source_lore:
        raise HTTPException(
            status_code=404,
            detail="Lore origem não encontrada",
        )

    if not target_lore:
        raise HTTPException(
            status_code=404,
            detail="Lore destino não encontrada",
        )

    if (
        source_lore.rpg_id
        != target_lore.rpg_id
    ):
        raise HTTPException(
            status_code=400,
            detail="As lores devem pertencer ao mesmo RPG",
        )

    if (
        source_lore.id
        == target_lore.id
    ):
        raise HTTPException(
            status_code=400,
            detail="Uma lore não pode se relacionar consigo mesma",
        )

    existing = (
        db.query(RPGLoreRelation)
        .filter(
            RPGLoreRelation.source_lore_id == source_lore.id,
            RPGLoreRelation.target_lore_id == target_lore.id,
        )
        .first()
    )

    if existing:
        return existing

    relation = RPGLoreRelation(
        source_lore_id=source_lore.id,
        target_lore_id=target_lore.id,
    )

    db.add(relation)
    db.commit()
    db.refresh(relation)

    return relation

@router.get(
    "/{lore_id}",
    response_model=list[LoreRelationDetailResponse],
)
def get_relations(
    lore_id: int,
    db: Session = Depends(get_db),
):
    lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.id == lore_id
        )
        .first()
    )

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore não encontrada",
        )

    return (
        db.query(RPGLoreRelation)
        .filter(
            RPGLoreRelation.source_lore_id
            == lore_id
        )
        .all()
    )