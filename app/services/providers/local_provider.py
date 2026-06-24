from app.services.providers.base_provider import (
    BaseProvider,
)

import requests


class LocalProvider(BaseProvider):

    def generate_text(
        self,
        prompt: str,
    ) -> str:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]