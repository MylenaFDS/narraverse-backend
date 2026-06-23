from abc import (
    ABC,
    abstractmethod,
)


class BaseProvider(
    ABC
):

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
    ):
        pass