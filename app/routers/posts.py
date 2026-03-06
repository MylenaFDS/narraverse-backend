from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post_service import PostService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])


# 🔹 CRIAR POST
@router.post("/", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PostService.create(db, post_data, current_user.id)


# 🔹 LISTAR TODOS
@router.get("/", response_model=List[PostResponse])
def list_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PostService.get_all(db)


# 🔹 BUSCAR POR ID
@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = PostService.get_by_id(db, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    return post


# 🔹 ATUALIZAR
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = PostService.get_by_id(db, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    # 🔒 Só dono pode editar
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return PostService.update(db, post_id, post_data)


# 🔹 DELETAR
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = PostService.get_by_id(db, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    # 🔒 Só dono pode deletar
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    PostService.delete(db, post_id)

    return {"message": "Post deletado com sucesso"}