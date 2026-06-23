from pydantic import BaseModel


class RPGSettingsUpdate(
    BaseModel
):
    use_ai_assistant: bool

    use_ai_narrator: bool

    use_ai_events: bool

    use_ai_npcs: bool


class RPGSettingsResponse(
    BaseModel
):
    id: int

    rpg_id: int

    use_ai_assistant: bool

    use_ai_narrator: bool

    use_ai_events: bool

    use_ai_npcs: bool

    class Config:
        from_attributes = True