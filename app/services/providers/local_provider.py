from app.services.providers.base_provider import (
    BaseProvider,
)


class LocalProvider(
    BaseProvider
):

    def generate_text(
        self,
        prompt: str,
    ):
        raise NotImplementedError