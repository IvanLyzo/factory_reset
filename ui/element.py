import pygame
from typing import Callable

class UIElement:

    def __init__(self, pos: pygame.math.Vector2, text: str, font: pygame.font.Font, callback: Callable[[], None] | None = None):
        self.pos: pygame.math.Vector2 = pos  # Center position of the text
        self.text: str = text  # Text to display
        self.font: pygame.font.Font = font  # Font used to render the text
        self.callback: Callable[[], None] | None = callback  # Optional function to call (e.g., on click)

    def draw(self, surface: pygame.Surface):
        
        # Render the text surface and center it at self.pos
        self.text_surface: pygame.Surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect: pygame.Rect = self.text_surface.get_rect(center=self.pos)

        # Draw the rendered text onto the target surface
        surface.blit(self.text_surface, self.text_rect)
