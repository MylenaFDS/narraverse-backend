class SceneContextBuilder:

    @staticmethod
    def build(
        scene,
        lore,
    ):
        return {
            "scene": {
                "id": scene.id,
                "title": scene.title,
                "description": scene.description,
            },
            "lore": {
                "id": lore.id,
                "title": lore.title,
                "description": lore.description,
            },
        }