class Scene:

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass  # Override in subclass

    def update(self, dt):
        pass  # Override in subclass

    def draw(self, screen):
        pass  # Override in subclass