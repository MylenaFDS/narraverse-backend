from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rpg import RPG
from app.models.rpg_participant import RPGParticipant
from app.models.tag import Tag
from app.schemas.rpg import RPGCreate, RPGResponse, RPGInvite
from app.models.user import User
from app.core.security import get_current_user
import shutil
import os


router = APIRouter(prefix="/rpgs", tags=["RPGs"])


@router.post("/", response_model=RPGResponse)
def create_rpg(
    rpg_data: RPGCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ Criar RPG
    new_rpg = RPG(
        name=rpg_data.name,
        description=rpg_data.description,
        owner_id=current_user.id,
        allow_join_requests=rpg_data.allow_join_requests
    )

    db.add(new_rpg)
    db.commit()
    db.refresh(new_rpg)

    # 🔥 2️⃣ Adicionar TAGS
    if rpg_data.tags:
        tag_objects = []

        for tag_name in rpg_data.tags:

            tag = db.query(Tag).filter(Tag.name == tag_name).first()

            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)

            tag_objects.append(tag)

        new_rpg.tags = tag_objects
        db.commit()
        db.refresh(new_rpg)

    # 3️⃣ Criador vira participante automaticamente
    owner_participation = RPGParticipant(
        user_id=current_user.id,
        rpg_id=new_rpg.id,
        status="accepted",
        invited_by=current_user.id,
    )

    db.add(owner_participation)
    db.commit()

    return new_rpg


@router.get("/me", response_model=list[RPGResponse])
def get_my_rpgs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rpgs = (
        db.query(RPG)
        .join(RPGParticipant, RPGParticipant.rpg_id == RPG.id)
        .filter(
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "accepted",
        )
        .all()
    )

    return [
        {
            **rpg.__dict__,
            "is_owner": rpg.owner_id == current_user.id
        }
        for rpg in rpgs
    ]

@router.post("/{rpg_id}/request")
def request_to_join(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ Verificar se RPG existe
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado.")

    # 2️⃣ Verificar se aceita pedidos
    if not rpg.allow_join_requests:
        raise HTTPException(
            status_code=403,
            detail="Este RPG não aceita pedidos de entrada."
        )

    # 3️⃣ Verificar se já existe participação
    existing = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == current_user.id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Você já possui uma solicitação ou participação."
        )

    # 4️⃣ Criar solicitação
    request = RPGParticipant(
        user_id=current_user.id,
        rpg_id=rpg_id,
        status="pending",
        invited_by=None,
    )

    db.add(request)
    db.commit()

    return {"message": "Solicitação enviada com sucesso."}


@router.get("/{rpg_id}/requests")
def list_pending_requests(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ Verificar se RPG existe
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado.")

    # 2️⃣ Verificar se é dono
    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode ver solicitações."
        )

    # 3️⃣ Buscar solicitações pendentes
    pending_requests = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.status == "pending",
        )
        .all()
    )

    return pending_requests


@router.put("/{rpg_id}/participants/{user_id}")
def update_participant_status(
    rpg_id: int,
    user_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ Validar status
    if status not in ["accepted", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status inválido. Use 'accepted' ou 'rejected'."
        )

    # 2️⃣ Verificar RPG
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado.")

    # 3️⃣ Verificar dono
    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode alterar participantes."
        )

    # 4️⃣ Buscar participante
    participant = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == user_id,
            RPGParticipant.status == "pending",
        )
        .first()
    )

    if not participant:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    # 5️⃣ Atualizar status
    participant.status = status
    db.commit()

    return {"message": f"Solicitação {status} com sucesso."}

# ======================================
# 📨 CONVIDAR PARTICIPANTE
# ======================================
@router.post("/{rpg_id}/invite")
def invite_participant(
    rpg_id: int,
    data: RPGInvite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # verificar RPG
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

    # apenas dono
    if rpg.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode convidar"
        )

    # usuário existe?
    user = (
        db.query(User)
        .filter(User.id == data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    # impedir duplicado
    existing = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == data.user_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Usuário já possui convite ou participação"
        )

    invite = RPGParticipant(
        user_id=data.user_id,
        rpg_id=rpg_id,
        status="invited",
        invited_by=current_user.id,
    )

    db.add(invite)
    db.commit()

    return {
        "message": "Convite enviado com sucesso"
    }

# ======================================
# 📨 MEUS CONVITES
# ======================================
@router.get("/invites")
def get_my_invites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    invites = (
        db.query(RPGParticipant, RPG)
        .join(
            RPG,
            RPG.id == RPGParticipant.rpg_id
        )
        .filter(
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "invited"
        )
        .all()
    )

    return [
        {
            "rpg_id": rpg.id,
            "rpg_name": rpg.name,
            "description": rpg.description,
            "status": participant.status,
        }
        for participant, rpg in invites
    ]

# ======================================
# ✅ ACEITAR CONVITE
# ======================================
@router.put("/invites/{rpg_id}/accept")
def accept_invite(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    participant = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "invited"
        )
        .first()
    )

    if not participant:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )

    participant.status = "accepted"

    db.commit()

    return {
        "message": "Convite aceito"
    }

# ======================================
# ❌ RECUSAR CONVITE
# ======================================
@router.put("/invites/{rpg_id}/reject")
def reject_invite(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    participant = (
        db.query(RPGParticipant)
        .filter(
            RPGParticipant.rpg_id == rpg_id,
            RPGParticipant.user_id == current_user.id,
            RPGParticipant.status == "invited"
        )
        .first()
    )

    if not participant:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )

    participant.status = "rejected"

    db.commit()

    return {
        "message": "Convite recusado"
    }

@router.get("/{rpg_id}", response_model=RPGResponse)
def get_rpg_by_id(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    return {
        **rpg.__dict__,
        "is_owner": rpg.owner_id == current_user.id
    }

@router.get("/{rpg_id}/me")
def get_my_role_in_rpg(
    rpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rpg = db.query(RPG).filter(RPG.id == rpg_id).first()

    if not rpg:
        raise HTTPException(status_code=404, detail="RPG não encontrado")

    return {
        "is_owner": rpg.owner_id == current_user.id
    }

@router.post("/{rpg_id}/map-image")
def upload_map_image(
    rpg_id: int,
    file: UploadFile = File(...),
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
            detail="Apenas o dono pode alterar o mapa"
        )

    os.makedirs("uploads/maps", exist_ok=True)

    filename = f"rpg_{rpg_id}.png"

    filepath = f"uploads/maps/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    rpg.world_map = filepath

    db.commit()

    return {
        "message": "Mapa enviado",
        "world_map": filepath,
    }