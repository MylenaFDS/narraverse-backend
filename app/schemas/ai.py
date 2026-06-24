from pydantic import BaseModel


class GenerateSceneRequest(
    BaseModel
):
    parent_scene_title: str
    parent_scene_description: str
    instruction: str

class GenerateLocationsRequest(
    BaseModel
):
    scene_title: str
    scene_description: str