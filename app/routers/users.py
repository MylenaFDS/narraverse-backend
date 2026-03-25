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
@router.get("/me", response_model=UserProfileResponse)
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # RPGs criados
    created = (
        db.query(RPG)
        .filter(RPG.owner_id == current_user.id)
        .all()
    )

    # RPGs participando
    participating = (
        db.query(RPG)
        .join(RPGParticipant)
        .filter(
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "accepted"
        )
        .all()
    )

    return {
        **current_user.__dict__,
        "created_rpgs": created,
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