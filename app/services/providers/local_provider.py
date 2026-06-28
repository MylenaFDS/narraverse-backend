import time
import requests

from app.services.providers.base_provider import (
    BaseProvider,
)

DEFAULT_SYSTEM_PROMPT = """
Você é a IA oficial do Narraverse.

Regras obrigatórias:

- Responda SEMPRE em português brasileiro.
- Nunca responda em inglês.
- Nunca explique o que está fazendo.
- Nunca use markdown.
- Nunca utilize ```json.
- Quando o usuário pedir JSON, responda SOMENTE JSON válido.
- Nunca escreva texto antes ou depois do JSON.
- Seja criativo, coerente e consistente com o universo apresentado.
"""


class LocalProvider(BaseProvider):

    def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        system_prompt = (
            system_prompt
            or DEFAULT_SYSTEM_PROMPT
        )

        print("=== ENVIANDO PARA OLLAMA ===")

        start = time.time()

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            },
            timeout=300,
        )

        print(
            f"Tempo: {time.time() - start:.2f}s"
        )

        response.raise_for_status()

        data = response.json()

        print("=== RESPOSTA BRUTA ===")
        print(data["message"]["content"])

        return data["message"]["content"]