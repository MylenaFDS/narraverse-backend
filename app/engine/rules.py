from app.engine.default_rules import (
    ActionResult,
    BaseRule,
)


class RuleEngine:

    def __init__(self):

        self.rules: dict[str, BaseRule] = {}

    # ------------------------------------
    # Registrar regra
    # ------------------------------------

    def register(
        self,
        rule: BaseRule,
    ):

        self.rules[
            rule.action
        ] = rule

    # ------------------------------------
    # Registrar várias
    # ------------------------------------

    def register_many(
        self,
        rules: list[BaseRule],
    ):

        for rule in rules:
            self.register(rule)

    # ------------------------------------
    # Executar ação
    # ------------------------------------

    def execute(
        self,
        action: str,
        actor: dict,
        target: dict | None = None,
        context: dict | None = None,
    ) -> ActionResult:

        context = context or {}

        rule = self.rules.get(action)

        if rule is None:

            return ActionResult(
                success=False,
                message=(
                    f"Nenhuma regra registrada "
                    f"para '{action}'."
                ),
            )

        return rule.execute(
            actor=actor,
            target=target,
            context=context,
        )

    # ------------------------------------
    # Existe regra?
    # ------------------------------------

    def has_rule(
        self,
        action: str,
    ) -> bool:

        return action in self.rules

    # ------------------------------------
    # Listar regras
    # ------------------------------------

    def list_rules(self):

        return sorted(
            self.rules.keys()
        )