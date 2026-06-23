class NarraverseAI:

    def generate_scene(
        self,
        context: dict,
        instruction: str,
    ):
        raise NotImplementedError

    def generate_npc(
        self,
        context: dict,
        instruction: str,
    ):
        raise NotImplementedError

    def generate_turn_help(
        self,
        context: dict,
        instruction: str,
    ):
        raise NotImplementedError

    def generate_event(
        self,
        context: dict,
    ):
        raise NotImplementedError