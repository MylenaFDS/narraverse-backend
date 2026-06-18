from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.rpg_lore import RPGLore, RPGLoreCategory
from app.models.rpg import RPG
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.models.map_region import MapRegion

from app.schemas.rpg_lore import (
    RPGLoreCreate,
    RPGLoreResponse,
    RPGLoreUpdate
)

from app.core.security import get_current_user

router = APIRouter(
    prefix="/rpg-lore",
    tags=["RPG Lore"]
)


# ======================================
# ✍️ CRIAR LORE / SUGESTÃO
# ======================================
@router.post(
    "/{rpg_id}",
    response_model=RPGLoreResponse
)
def create_lore(
    rpg_id: int,
    data: RPGLoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    # 🔥 dono cria direto
    if rpg.owner_id == current_user.id:

        lore = RPGLore(
            title=data.title,
            content=data.content,
            visual_description=data.visual_description,
            category=data.category,
            rpg_id=rpg_id,
            author_id=current_user.id,
            is_approved=True,
            is_suggestion=False
)

    else:
        # verificar participação
        participant = (
            db.query(RPGParticipant)
            .filter(
                RPGParticipant.rpg_id == rpg_id,
                RPGParticipant.user_id == current_user.id,
                RPGParticipant.status == "accepted"
            )
            .first()
        )

        if not participant:
            raise HTTPException(
                status_code=403,
                detail="Você não participa deste RPG"
            )

        # verificar se sugestões são permitidas
        if not rpg.allow_lore_suggestions:
            raise HTTPException(
                status_code=403,
                detail="Este RPG não permite sugestões de lore"
            )

        lore = RPGLore(
            title=data.title,
            content=data.content,
            category=data.category,
            rpg_id=rpg_id,
            author_id=current_user.id,
            is_approved=False,
            is_suggestion=True
        )

    db.add(lore)
    db.commit()
    db.refresh(lore)

    if lore.category == "Mundo" and lore.is_approved:
        existing_region = (
            db.query(MapRegion)
            .filter(
                MapRegion.rpg_id == rpg_id,
                MapRegion.lore_id == lore.id,
            )
            .first()
        )

        if not existing_region:
            region = MapRegion(
                name=lore.title,
                lore_id=lore.id,
                rpg_id=rpg_id,
                pos_x=50,
                pos_y=50,
                color="#e0a96d",
            )

            db.add(region)
            db.commit()

    return lore


# ======================================
# 📖 LISTAR LORE APROVADA
# ======================================
@router.get(
    "/{rpg_id}",
    response_model=list[RPGLoreResponse]
)
def list_lore(
    rpg_id: int,
    db: Session = Depends(get_db)
):

    lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.rpg_id == rpg_id,
            RPGLore.is_approved == True
        )
        .all()
    )

    return lore


# ======================================
# 📨 LISTAR SUGESTÕES
# ======================================
@router.get(
    "/{rpg_id}/suggestions",
    response_model=list[RPGLoreResponse]
)
def list_suggestions(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode ver sugestões"
        )

    suggestions = (
        db.query(RPGLore)
        .filter(
            RPGLore.rpg_id == rpg_id,
            RPGLore.is_suggestion == True,
            RPGLore.is_approved == False
        )
        .all()
    )

    return suggestions


# ======================================
# ✅ APROVAR SUGESTÃO
# ======================================
@router.put("/{lore_id}/approve")
def approve_lore(
    lore_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    lore = (
        db.query(RPGLore)
        .filter(RPGLore.id == lore_id)
        .first()
    )

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore não encontrada"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == lore.rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode aprovar"
        )

    lore.is_approved = True
    lore.is_suggestion = False

    db.commit()

    return {
        "message": "Lore aprovada com sucesso"
    }
@router.post("/{rpg_id}/sync-map-regions")
def sync_map_regions(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode sincronizar regiões"
        )

    world_lore = (
        db.query(RPGLore)
        .filter(
            RPGLore.rpg_id == rpg_id,
            RPGLore.category == "Mundo",
            RPGLore.is_approved == True,
        )
        .all()
    )

    created_count = 0

    for index, lore in enumerate(world_lore):
        existing_region = (
            db.query(MapRegion)
            .filter(
                MapRegion.rpg_id == rpg_id,
                MapRegion.lore_id == lore.id,
            )
            .first()
        )

        if existing_region:
            continue

        region = MapRegion(
            name=lore.title,
            lore_id=lore.id,
            rpg_id=rpg_id,
            pos_x=20 + ((index * 13) % 60),
            pos_y=20 + ((index * 17) % 60),
            color="#e0a96d",
        )

        db.add(region)
        created_count += 1

    db.commit()

    return {
        "message": "Regiões sincronizadas",
        "created": created_count,
    }

# ======================================
# 📂 CATEGORY SCHEMA
# ======================================
class CategoryCreate(BaseModel):
    name: str


# ======================================
# ➕ CRIAR CATEGORIA
# ======================================
@router.post("/{rpg_id}/categories")
def create_category(
    rpg_id: int,
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    rpg = (
        db.query(RPG)
        .filter(RPG.id == rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode criar categorias"
        )

    existing = (
        db.query(RPGLoreCategory)
        .filter(
            RPGLoreCategory.rpg_id == rpg_id,
            RPGLoreCategory.name == data.name
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Categoria já existe"
        )

    category = RPGLoreCategory(
        name=data.name,
        rpg_id=rpg_id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# ======================================
# 📂 LISTAR CATEGORIAS
# ======================================
@router.get("/{rpg_id}/categories")
def get_categories(
    rpg_id: int,
    db: Session = Depends(get_db)
):

    categories = (
        db.query(RPGLoreCategory)
        .filter(
            RPGLoreCategory.rpg_id == rpg_id
        )
        .all()
    )

    return [c.name for c in categories]

# ======================================
# ✏️ EDITAR LORE
# ======================================
@router.put("/{lore_id}")
def update_lore(
    lore_id: int,
    data: RPGLoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    lore = (
        db.query(RPGLore)
        .filter(RPGLore.id == lore_id)
        .first()
    )

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore não encontrada"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == lore.rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    # só dono pode editar
    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode editar"
        )

    lore.title = data.title
    lore.content = data.content
    lore.visual_description = (
        data.visual_description
    )
    lore.category = data.category

    db.commit()
    db.refresh(lore)

    return lore

# ======================================
# 🗑️ DELETAR LORE
# ======================================
@router.delete("/{lore_id}")
def delete_lore(
    lore_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    lore = (
        db.query(RPGLore)
        .filter(RPGLore.id == lore_id)
        .first()
    )

    if not lore:
        raise HTTPException(
            status_code=404,
            detail="Lore não encontrada"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == lore.rpg_id)
        .first()
    )

    if not rpg:
        raise HTTPException(
            status_code=404,
            detail="RPG não encontrado"
        )

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode deletar"
        )

    # 🔥 remove regiões ligadas à lore
    db.query(MapRegion).filter(
        MapRegion.lore_id == lore.id
    ).delete()

    # 🔥 remove lore
    db.delete(lore)

    db.commit()

    return {
        "message": "Lore deletada"
    }