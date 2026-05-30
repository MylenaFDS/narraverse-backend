from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.rpg import RPG
from app.models.rpg_note import RPGNote

from app.schemas.rpg_note import (
    RPGNoteCreate,
    RPGNoteUpdate,
    RPGNoteResponse,
)

router = APIRouter(
    prefix="/notes",
    tags=["RPG Notes"]
)

@router.get(
    "/rpg/{rpg_id}",
    response_model=list[RPGNoteResponse]
)
def get_notes(
    rpg_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RPGNote)
        .filter(RPGNote.rpg_id == rpg_id)
        .order_by(RPGNote.id.desc())
        .all()
    )

@router.post(
    "/rpg/{rpg_id}",
    response_model=RPGNoteResponse
)
def create_note(
    rpg_id: int,
    data: RPGNoteCreate,
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
            detail="Apenas o dono do RPG pode criar anotações"
        )

    note = RPGNote(
        title=data.title,
        content=data.content,
        rpg_id=rpg_id,
        author_id=current_user.id,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note

@router.put(
    "/{note_id}",
    response_model=RPGNoteResponse
)
def update_note(
    note_id: int,
    data: RPGNoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(RPGNote)
        .filter(RPGNote.id == note_id)
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Nota não encontrada"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == note.rpg_id)
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
            detail="Apenas o dono do RPG pode editar anotações"
        )

    note.title = data.title
    note.content = data.content

    db.commit()
    db.refresh(note)

    return note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(RPGNote)
        .filter(RPGNote.id == note_id)
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Nota não encontrada"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == note.rpg_id)
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
            detail="Apenas o dono do RPG pode excluir anotações"
        )

    db.delete(note)
    db.commit()

    return {
        "message": "Nota excluída com sucesso"
    }