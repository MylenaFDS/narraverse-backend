import re


class Interpreter:

    """
    Converte linguagem natural em ações do Engine.
    """

    ATTACK = [
        "ataco",
        "atacar",
        "golpeio",
        "bato",
        "esfaqueio",
        "acerto",
        "disparo",
    ]

    DEFEND = [
        "defendo",
        "defender",
        "protejo",
        "bloqueio",
    ]

    HEAL = [
        "curo",
        "curar",
        "trato",
        "restauro",
    ]

    PERSUASION = [
        "convenço",
        "persuado",
        "negocio",
        "converso",
    ]

    def interpret(
        self,
        text: str,
    ) -> dict:

        original = text

        text = text.lower().strip()

        # -------------------------------
        # ATAQUE
        # -------------------------------

        if any(word in text for word in self.ATTACK):

            target = self._extract_target(text)

            return {
                "action": "attack",
                "target": target,
                "raw": original,
            }

        # -------------------------------
        # DEFESA
        # -------------------------------

        if any(word in text for word in self.DEFEND):

            return {
                "action": "defend",
                "raw": original,
            }

        # -------------------------------
        # CURA
        # -------------------------------

        if any(word in text for word in self.HEAL):

            target = self._extract_target(text)

            return {
                "action": "heal",
                "target": target,
                "raw": original,
            }

        # -------------------------------
        # PERSUASÃO
        # -------------------------------

        if any(word in text for word in self.PERSUASION):

            target = self._extract_target(text)

            return {
                "action": "persuasion",
                "target": target,
                "raw": original,
            }

        # -------------------------------
        # FALLBACK
        # -------------------------------

        return {
            "action": "unknown",
            "raw": original,
        }

    def _extract_target(
        self,
        text: str,
    ) -> str | None:

        match = re.search(
            r"(?:em|no|na|contra|o|a)\s+(.+)",
            text,
        )

        if not match:
            return None

        return match.group(1).strip()