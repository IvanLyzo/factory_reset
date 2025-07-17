import pygame

from constants import *

class Button:

    def __init__(self, pos, text, font, width=60, height=24, callback=None):
        self.rect = pygame.Rect(pos[0] - width / 2, pos[1] - height / 2, width, height)
        self.text = text
        self.font = font

        self.callback = callback

        # Prepare text by rendering to other surface
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = (event.pos[0] / SCREEN_SCALE, event.pos[1] / SCREEN_SCALE)
            if self.rect.collidepoint(pos):
                print("pressed")

                if self.callback:
                    self.callback()
    
    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        surface.blit(self.text_surface, self.text_rect)