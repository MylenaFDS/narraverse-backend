from app.services.providers.local_provider import (
    LocalProvider,
)


class NarraverseAI:

    def __init__(self):
        self.provider = LocalProvider()

    def generate_scene(
        self,
        context: str,
        instruction: str,
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

    def generate_hotspots(
        self,
        scene_title: str,
        scene_description: str,
    ):
        prompt = f"""
Você é a IA oficial do Narraverse.

RESPONDA SEMPRE EM PORTUGUÊS DO BRASIL.

Sua função é criar hotspots navegáveis.

IMPORTANTE:

- Os hotspots devem existir DENTRO da cena.
- Não crie locais externos.
- Não crie cidades.
- Não crie regiões.
- Não crie florestas.
- Não crie jardins.
- Não crie construções completas.
- Não use locais famosos de livros, filmes ou jogos.

Os hotspots devem representar
objetos, áreas ou pontos específicos
que podem ser explorados.

Exemplos:

Cozinha:
- Forno
- Despensa
- Mesa de refeições
- Armário de ingredientes
- Adega

Biblioteca:
- Estante principal
- Escrivaninha
- Cofre
- Escada móvel
- Mesa de leitura

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

Crie exatamente 5 hotspots.
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

RESPONDA SOMENTE EM PORTUGUÊS.

Sua função é criar novas cenas
conectadas à cena atual.

Retorne SOMENTE JSON.

Formato:

[
  {{
    "title": "...",
    "description": "..."
  }}
]

Cena atual:
{scene_title}

Descrição:
{scene_description}

Crie exatamente 5 possíveis cenas filhas.
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