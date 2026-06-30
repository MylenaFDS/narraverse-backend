from dataclasses import dataclass
from typing import Any


@dataclass
class ActionResult:
    success: bool
    message: str
    data: dict | None = None


class BaseRule:
    """
    Classe base de todas as regras.
    """

    action: str = ""

    def execute(
        self,
        actor: dict,
        target: dict | None,
        context: dict,
    ) -> ActionResult:
        raise NotImplementedError


# ==========================================================
# ATAQUE
# ==========================================================

class AttackRule(BaseRule):

    action = "attack"

    def execute(
        self,
        actor,
        target,
        context,
    ) -> ActionResult:

        if target is None:
            return ActionResult(
                success=False,
                message="Nenhum alvo informado."
            )

        return ActionResult(
            success=True,
            message=f"{actor['name']} atacou {target['name']}.",
            data={
                "damage": None,
            },
        )


# ==========================================================
# DEFESA
# ==========================================================

class DefendRule(BaseRule):

    action = "defend"

    def execute(
        self,
        actor,
        target,
        context,
    ) -> ActionResult:

        return ActionResult(
            success=True,
            message=f"{actor['name']} entrou em posição defensiva."
        )


# ==========================================================
# CURA
# ==========================================================

class HealRule(BaseRule):

    action = "heal"

    def execute(
        self,
        actor,
        target,
        context,
    ) -> ActionResult:

        if target is None:
            target = actor

        return ActionResult(
            success=True,
            message=f"{actor['name']} curou {target['name']}."
        )


# ==========================================================
# TESTE DE ATRIBUTO
# ==========================================================

class AttributeTestRule(BaseRule):

    action = "attribute_test"

    def execute(
        self,
        actor,
        target,
        context,
    ) -> ActionResult:

        attribute = context.get("attribute")

        return ActionResult(
            success=True,
            message=(
                f"{actor['name']} realizou um teste de "
                f"{attribute}."
            ),
        )


# ==========================================================
# PERSUASÃO
# ==========================================================

class PersuasionRule(BaseRule):

    action = "persuasion"

    def execute(
        self,
        actor,
        target,
        context,
    ) -> ActionResult:

        if target is None:
            return ActionResult(
                success=False,
                message="Nenhum alvo informado."
            )

        return ActionResult(
            success=True,
            message=(
                f"{actor['name']} tentou convencer "
                f"{target['name']}."
            ),
        )


# ==========================================================
# REGISTRY
# ==========================================================

DEFAULT_RULES = [
    AttackRule(),
    DefendRule(),
    HealRule(),
    AttributeTestRule(),
    PersuasionRule(),
]