from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.schemas.user import UserResponse, UserUpdate, UserProfileResponse
from app.services.user_service import UserService
from app.core.security import get_current_user
from app.models.user import User
from app.models.rpg import RPG
from app.models.rpg_participant import RPGParticipant


router = APIRouter(prefix="/users", tags=["Users"])


# 🔹 LISTAR TODOS
@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserService.get_all(db)


# 🔹 USUÁRIO LOGADO
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    owned_rpgs = db.query(RPG).filter(RPG.owner_id == current_user.id).all()

    participating = (
        db.query(RPG)
        .join(RPGParticipant)
        .filter(RPGParticipant.user_id == current_user.id)
        .all()
    )

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "bio": current_user.bio,
        "owned_rpgs": owned_rpgs,  # 🔥 ESSENCIAL
        "participating_rpgs": participating
    }

# 🔥 🔹 ATUALIZAR PERFIL (MELHOR PRÁTICA)
@router.put("/me", response_model=UserResponse)
def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_user = UserService.update(db, current_user.id, user_data)

    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return updated_user

@router.get("/{user_id}/profile")
def get_public_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    owned_rpgs = (
        db.query(RPG)
        .filter(RPG.owner_id == user.id)
        .all()
    )

    participating_rpgs = (
        db.query(RPG)
        .join(RPGParticipant)
        .filter(
            RPGParticipant.user_id == user.id,
            RPGParticipant.status == "accepted",
            RPG.owner_id != user.id,
        )
        .all()
    )

    return {
        "id": user.id,
        "username": user.username,
        "bio": user.bio,
        "owned_rpgs": [
            {
                "id": rpg.id,
                "name": rpg.name,
                "description": rpg.description,
                "banner_url": rpg.banner_url,
            }
            for rpg in owned_rpgs
        ],
        "participating_rpgs": [
            {
                "id": rpg.id,
                "name": rpg.name,
                "description": rpg.description,
                "banner_url": rpg.banner_url,
            }
            for rpg in participating_rpgs
        ],
    }
# 🔹 BUSCAR POR ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = UserService.get_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


# 🔹 ATUALIZAR (mantido, mas menos usado agora)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    user = UserService.update(db, user_id, user_data)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


# 🔹 DELETAR
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    success = UserService.delete(db, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"message": "Usuário deletado com sucesso"}