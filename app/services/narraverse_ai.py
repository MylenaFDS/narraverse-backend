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
Você é a IA oficial do Narraverse.

RESPONDA SEMPRE EM PORTUGUÊS DO BRASIL.

Crie conteúdo criativo para RPG.

Contexto:

{context}

Pedido:

{instruction}
"""

        return self.provider.generate_text(
            prompt
        )

    def generate_locations(
    self,
    scene_title: str,
    scene_description: str,
):
        prompt = f"""
    Você é a IA oficial do Narraverse.

    Responda SOMENTE em português.

    Sua função é criar hotspots navegáveis.

    IMPORTANTE:

    - Os locais devem existir DENTRO da cena.
    - Não crie locais externos.
    - Não crie cidades.
    - Não crie regiões.
    - Não crie florestas.
    - Não crie jardins.
    - Não crie locais genéricos.
    - Não use locais famosos de livros, filmes ou jogos.

    Cada local deve representar um ponto específico
    que o jogador pode explorar.

    Exemplo para uma cozinha:

    - Despensa
    - Forno
    - Mesa de refeições
    - Armário de ingredientes
    - Adega

    Retorne SOMENTE JSON.

    Formato:

    [
    {{
        "name": "...",
        "description": "..."
    }}
    ]

    Cena:
    {scene_title}

    Descrição:
    {scene_description}

    Crie exatamente 5 locais.
    """
        return self.provider.generate_text(prompt)
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