from app.services.providers.local_provider import (
    LocalProvider,
)


class NarraverseAI:

    def __init__(self):
        self.provider = LocalProvider()

    def generate_scene(
        self,
        context,
        instruction,
    ):
        prompt = f"""
Contexto:

{context}

Pedido:

{instruction}
"""

        return self.provider.generate_text(
            prompt
        )
    def generate_npc(
        self,
        context: dict,
        instruction: str,
    ):
        raise NotImplementedError

    def generate_turn_help(
        self,
        context: dict,
        instruction: str,
    ):
        raise NotImplementedError

    def generate_event(
        self,
        context: dict,
    ):
        raise NotImplementedError