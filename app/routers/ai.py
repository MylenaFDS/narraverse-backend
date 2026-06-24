from fastapi import APIRouter

from app.schemas.ai import (
    GenerateSceneRequest,
    GenerateLocationsRequest,
    GenerateHotspotsRequest,
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


@router.post("/generate-hotspots")
def generate_hotspots_ai(
    data: GenerateHotspotsRequest,
):
    ai = NarraverseAI()

    response = ai.generate_hotspots(
        scene_title=data.scene_title,
        scene_description=data.scene_description,
    )

    return {
        "response": response
    }


@router.post("/generate-locations")
def generate_locations_ai(
    data: GenerateLocationsRequest,
):
    ai = NarraverseAI()

    response = ai.generate_locations(
        scene_title=data.scene_title,
        scene_description=data.scene_description,
    )

    return {
        "response": response
    }