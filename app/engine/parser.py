from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParsedCharacter:
    """
    Representação padronizada de um personagem.

    Independentemente do sistema utilizado
    (D&D, Tordem, Ordem, sistema próprio etc.),
    a Engine trabalhará sempre com esta estrutura.
    """

    id: int | None = None

    name: str = ""

    attributes: dict[str, float] = field(default_factory=dict)

    resources: dict[str, float] = field(default_factory=dict)

    skills: dict[str, float] = field(default_factory=dict)

    inventory: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)


class CharacterParser:
    """
    Converte qualquer ficha para um formato
    compreendido pela Narraverse Engine.
    """

    def parse(
        self,
        character: Any,
        sheet_fields: list[Any],
    ) -> ParsedCharacter:

        parsed = ParsedCharacter()

        parsed.id = getattr(character, "id", None)
        parsed.name = getattr(character, "name", "")

        for field in sheet_fields:

            category = (
                getattr(field, "category", "")
                or ""
            ).lower()

            name = (
                getattr(field, "name", "")
                or ""
            ).strip()

            value = getattr(field, "value", None)

            if category == "atributo":
                parsed.attributes[name] = self._number(value)

            elif category == "recurso":
                parsed.resources[name] = self._number(value)

            elif category == "perícia":
                parsed.skills[name] = self._number(value)

            elif category == "inventário":
                parsed.inventory[name] = value

            else:
                parsed.metadata[name] = value

        return parsed

    def _number(
        self,
        value: Any,
    ) -> float:

        if value is None:
            return 0

        try:
            return float(value)

        except Exception:
            return 0