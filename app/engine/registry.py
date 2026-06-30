from app.engine.rules import RuleEngine

from app.engine.default_rules import (
    DEFAULT_RULES,
)


def build_engine():

    engine = RuleEngine()

    engine.register_many(
        DEFAULT_RULES
    )

    return engine