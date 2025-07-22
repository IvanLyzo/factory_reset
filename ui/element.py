import pygame
from typing import Callable

class UIElement:

    def __init__(self, pos: pygame.math.Vector2, text: str, font: pygame.font.Font, callback: Callable[[], None] | None = None):
        self.pos: pygame.math.Vector2 = pos
        self.text: str = text
        self.font: pygame.font.Font = font
        self.callback: Callable[[], None] | None = callback

        self.text_surface: pygame.Surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect: pygame.Rect = self.text_surface.get_rect(center=self.pos)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.text_surface, self.text_rect)
