class OptionsScene:

    def __init__(self, game):
        self.game = game
        pass

    def handle_event(self, event):
        pass  # Override in subclass

    def update(self, dt):
        pass  # Override in subclass

    def draw(self, screen):
        pass  # Override in subclass