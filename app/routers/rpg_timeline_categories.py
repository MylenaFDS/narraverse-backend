from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.rpg import RPG
from app.models.rpg_timeline_category import (
    RPGTimelineCategory,
)

from app.schemas.rpg_timeline_category import (
    TimelineCategoryCreate,
    TimelineCategoryResponse,
)


router = APIRouter(
    prefix="/timeline-categories",
    tags=["Timeline Categories"],
)

@router.get(
    "/rpg/{rpg_id}",
    response_model=list[
        TimelineCategoryResponse
    ],
)
def get_categories(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(
            RPGTimelineCategory
        )
        .filter(
            RPGTimelineCategory.rpg_id
            == rpg_id
        )
        .order_by(
            RPGTimelineCategory.name.asc()
        )
        .all()
    )

@router.post(
    "/rpg/{rpg_id}",
    response_model=
    TimelineCategoryResponse,
)
def create_category(
    rpg_id: int,
    data: TimelineCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    rpg = (
        db.query(RPG)
        .filter(
            RPG.id == rpg_id
        )
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado",
        )

    if (
        rpg.owner_id
        != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Sem permissão",
        )

    existing = (
        db.query(
            RPGTimelineCategory
        )
        .filter(
            RPGTimelineCategory.rpg_id
            == rpg_id,
            RPGTimelineCategory.name
            == data.name,
        )
        .first()
    )

    if existing:
        return existing

    category = RPGTimelineCategory(
            name=data.name,
            rpg_id=rpg_id,
        )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    category = (
        db.query(
            RPGTimelineCategory
        )
        .filter(
            RPGTimelineCategory.id
            == category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada",
        )

    rpg = (
        db.query(RPG)
        .filter(
            RPG.id == category.rpg_id
        )
        .first()
    )

    if (
        not rpg
        or rpg.owner_id
        != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Sem permissão",
        )

    db.delete(category)
    db.commit()

    return {
        "message":
        "Categoria removida"
    }