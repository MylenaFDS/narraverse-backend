import json
import re

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
Você é um gerador JSON.

REGRAS OBRIGATÓRIAS:

- Responda SOMENTE JSON.
- Não explique nada.
- Não escreva frases antes.
- Não escreva frases depois.
- Não use markdown.
- Não use ```json.
- Não escreva "Aqui está o resultado".
- Não escreva comentários.

Os hotspots devem existir DENTRO da cena.

Não crie:
- cidades
- regiões
- florestas
- jardins
- construções completas

Crie pontos específicos exploráveis.

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

Formato obrigatório:

[
  {{
    "name": "Nome",
    "description": "Descrição"
  }}
]

Cena:
{scene_title}

Descrição:
{scene_description}

Crie exatamente 5 hotspots.
"""

        response = self.provider.generate_text(
            prompt
        )

        try:
            match = re.search(
                r"\[.*\]",
                response,
                re.DOTALL,
            )

            if match:
                return json.loads(
                    match.group(0)
                )
                
            

            return []
                

        except Exception:
            return []

    def generate_locations(
        self,
        scene_title: str,
        scene_description: str,
    ):
        prompt = f"""
Você é um gerador JSON.

REGRAS OBRIGATÓRIAS:

- Responda SOMENTE JSON.
- Não explique nada.
- Não use markdown.
- Não escreva frases extras.

Formato:

[
  {{
    "title": "Título",
    "description": "Descrição"
  }}
]

Cena atual:
{scene_title}

Descrição:
{scene_description}

Crie exatamente 5 possíveis cenas filhas.
"""

        response = self.provider.generate_text(
            prompt
        )

        try:
            match = re.search(
                r"\[.*\]",
                response,
                re.DOTALL,
            )

            if match:
                return json.loads(
                    match.group(0)
                )

            return []

        except Exception:
            return []

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
    
    def generate_lore(
    self,
    category: str,
    theme: str,
    style: str | None = None,
    required_elements: str | None = None,
):
        prompt = f"""
    Você é a IA oficial do Narraverse.

    REGRAS OBRIGATÓRIAS:

    - Responda SOMENTE JSON.
    - Responda SEMPRE em português do Brasil.
    - Não explique nada.
    - Não use markdown.
    - Não escreva frases antes ou depois do JSON.
    - Não utilize ```json.

    Crie uma lore completa para um RPG.

    Categoria:
    {category}

    Tema:
    {theme}

    Estilo:
    {style or "Livre"}

    Elementos obrigatórios:
    {required_elements or "Nenhum"}

    Formato obrigatório:

    {{
    "title": "...",
    "description": "...",
    "history": "...",
    "culture": "...",
    "appearance": "...",
    "curiosities": "...",
    "economy": "...",
    "religion": "..."
    }}

    Observações:

    - Se algum campo não fizer sentido para esta categoria, retorne uma string vazia ("").
    - O título deve ser curto.
    - A descrição deve ter entre 2 e 4 parágrafos.
    - A história deve ser rica em detalhes.
    - O conteúdo deve ser coerente com fantasia medieval, salvo indicação diferente no tema.
    """

        response = self.provider.generate_text(prompt)

        try:
            match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL,
            )

            if match:
                return json.loads(match.group(0))

            return {}

        except Exception:
            return {}