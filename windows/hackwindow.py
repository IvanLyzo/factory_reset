import pygame

from ui.window import Window

class HackWindow(Window):

    def __init__(self):
        super().__init__(40)

    def handle_event(self, event: pygame.event.Event):
        pass  # Override in subclass

    def update(self, dt: float):
        pass  # Override in subclass

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)