from app.services.ai_provider import (
    generate_text,
)

def generate_scene(
    parent_title: str,
    parent_description: str,
    instruction: str,
):
    prompt = f"""
Você é um mestre de RPG.

Cena atual:
{parent_title}

Descrição:
{parent_description}

Pedido:
{instruction}

Retorne SOMENTE JSON:

{{
  "title": "...",
  "description": "...",
  "image_prompt": "..."
}}
"""

    return generate_text(prompt)