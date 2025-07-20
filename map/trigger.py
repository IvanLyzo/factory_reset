class Trigger:
    def __init__(self, rect, on_enter):
        self.rect = rect
        self.on_enter = on_enter

        self.triggered = False

    def check(self, player):
        if self.rect.colliderect(player.rect):
            if not self.triggered:
                self.on_enter()  # Call the event
                self.triggered = True
        else:
            self.triggered = False  # Reset when player leaves