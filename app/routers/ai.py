from fastapi import APIRouter
from app.schemas.ai import (
    GenerateSceneRequest,
)

from app.services.narraverse_ai import (
    NarraverseAI,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

@router.get("/status")
def ai_status():
    return {
        "provider": "local",
        "status": "ready",
    }

@router.post("/generate-scene")
def generate_scene_ai(
    data: GenerateSceneRequest,
):
    ai = NarraverseAI()

    context = f"""
Título:
{data.parent_scene_title}

Descrição:
{data.parent_scene_description}
"""

    response = ai.generate_scene(
        context=context,
        instruction=data.instruction,
    )

    return {
        "response": response
    }
