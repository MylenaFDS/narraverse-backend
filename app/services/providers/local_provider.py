import time
import requests

from app.services.providers.base_provider import (
    BaseProvider,
)


class LocalProvider(BaseProvider):

    def generate_text(
        self,
        prompt: str,
    ) -> str:

        print("=== ENVIANDO PARA OLLAMA ===")

        start = time.time()

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        print(
            f"Tempo: {time.time() - start:.2f}s"
        )

        response.raise_for_status()

        data = response.json()

        print("=== RESPOSTA RECEBIDA ===")

        return data["response"]