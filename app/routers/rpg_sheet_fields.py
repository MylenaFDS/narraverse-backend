from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg import RPG
from app.models.rpg_sheet_field import RPGSheetField
from app.models.user import User
from app.schemas.rpg_sheet_field import RPGSheetFieldCreate, RPGSheetFieldResponse
from app.models.character_sheet_value import CharacterSheetValue
from app.core.security import get_current_user

router = APIRouter(prefix="/rpg-sheet-fields", tags=["RPG Sheet Fields"])


@router.post("/{rpg_id}", response_model=RPGSheetFieldResponse)
def create_field(
    rpg_id: int,
    field_data: RPGSheetFieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o criador do RPG pode definir os campos da ficha"
        )

    field = RPGSheetField(
        rpg_id=rpg_id,
        name=field_data.name,
        field_type=field_data.field_type
    )

    db.add(field)
    db.commit()
    db.refresh(field)

    return field


@router.get("/{rpg_id}", response_model=list[RPGSheetFieldResponse])
def list_fields(
    rpg_id: int,
    db: Session = Depends(get_db)
):

    fields = (
        db.query(RPGSheetField)
        .filter(RPGSheetField.rpg_id == rpg_id)
        .all()
    )

    
    return fields

@router.put("/{field_id}", response_model=RPGSheetFieldResponse)
def update_field(
    field_id: int,
    field_data: RPGSheetFieldCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    field = (
        db.query(RPGSheetField)
        .filter(RPGSheetField.id == field_id)
        .first()
    )

    if not field:
        raise HTTPException(
            status_code=404,
            detail="Campo não encontrado"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == field.rpg_id)
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
            detail="Apenas o criador do RPG pode editar os campos da ficha"
        )

    field.name = field_data.name

    db.commit()
    db.refresh(field)

    return field

@router.delete("/{field_id}")
def delete_field(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    field = (
        db.query(RPGSheetField)
        .filter(RPGSheetField.id == field_id)
        .first()
    )

    if not field:
        raise HTTPException(
            status_code=404,
            detail="Campo não encontrado"
        )

    rpg = (
        db.query(RPG)
        .filter(RPG.id == field.rpg_id)
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
            detail="Apenas o criador do RPG pode excluir os campos da ficha"
        )
    
    db.query(CharacterSheetValue).filter(
    CharacterSheetValue.field_id == field.id
    ).delete()
    db.delete(field)
    db.commit()

    return {"message": "Campo excluído com sucesso"}