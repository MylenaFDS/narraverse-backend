from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg_lore import RPGLore
from app.models.rpg import RPG
from app.models.rpg_participant import RPGParticipant
from app.models.user import User
from app.schemas.rpg_lore import RPGLoreCreate, RPGLoreResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/rpg-lore", tags=["RPG Lore"])


# 🔥 Criar lore ou sugestão
@router.post("/{rpg_id}", response_model=RPGLoreResponse)
def create_lore(
    rpg_id: int,
    data: RPGLoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    # 🔥 Se for dono → cria direto aprovado
    if rpg.owner_id == current_user.id:

        lore = RPGLore(
            title=data.title,
            content=data.content,
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
            rpg_id=rpg_id,
            author_id=current_user.id,
            is_approved=False,
            is_suggestion=True
        )

    db.add(lore)
    db.commit()
    db.refresh(lore)

    return lore


# 📖 Listar lore aprovada (público)
@router.get("/{rpg_id}", response_model=list[RPGLoreResponse])
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


# 📨 Listar sugestões (apenas dono)
@router.get("/{rpg_id}/suggestions", response_model=list[RPGLoreResponse])
def list_suggestions(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

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


# ✅ Aprovar sugestão
@router.put("/{lore_id}/approve")
def approve_lore(
    lore_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    lore = db.query(RPGLore).filter(RPGLore.id == lore_id).first()

    if not lore:
        raise HTTPException(status_code=404, detail="Lore não encontrada")

    rpg = db.query(RPG).filter(RPG.id == lore.rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode aprovar"
        )

    # 🔥 atualiza status corretamente
    lore.is_approved = True
    lore.is_suggestion = False

    db.commit()

    return {"message": "Lore aprovada com sucesso"}