from dataclasses import dataclass, field
from typing import Any


@dataclass
class NarrativeContext:
    """
    Contexto completo utilizado pela Narraverse Engine.

    Toda decisão da Engine é baseada neste objeto.
    Ele não depende do banco de dados nem de SQLAlchemy.
    """

    # RPG atual
    rpg: Any | None = None

    # Cena atual
    scene: Any | None = None

    # Turno atual
    turn: Any | None = None

    # Personagem ativo
    character: Any | None = None

    # Usuário ativo
    user: Any | None = None

    # Região atual
    region: Any | None = None

    # Facção atual
    faction: Any | None = None

    # Evento atual
    event: Any | None = None

    # Listas disponíveis
    characters: list[Any] = field(default_factory=list)
    factions: list[Any] = field(default_factory=list)
    lore: list[Any] = field(default_factory=list)
    events: list[Any] = field(default_factory=list)
    npcs: list[Any] = field(default_factory=list)

    # Variáveis livres da Engine
    variables: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        """
        Recupera uma variável dinâmica.
        """
        return self.variables.get(key, default)

    def set(self, key: str, value: Any):
        """
        Define uma variável dinâmica.
        """
        self.variables[key] = value

    def has(self, key: str) -> bool:
        """
        Verifica se uma variável existe.
        """
        return key in self.variables

    def remove(self, key: str):
        """
        Remove uma variável dinâmica.
        """
        self.variables.pop(key, None)

    def clear_variables(self):
        """
        Limpa todas as variáveis temporárias.
        """
        self.variables.clear()