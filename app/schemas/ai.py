from pydantic import BaseModel


class GenerateSceneRequest(
    BaseModel
):
    parent_scene_title: str
    parent_scene_description: str
    instruction: str