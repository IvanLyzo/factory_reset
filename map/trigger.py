import pygame

from collections.abc import Callable

from entities.player import Player

class Trigger:
    def __init__(self, rect: pygame.Rect, on_enter: Callable[[], None]):
        self.rect: pygame.Rect = rect
        self.on_enter: Callable[[], None] = on_enter

        self.triggered: bool = False

    def check(self, player: Player):
        if self.rect.colliderect(player.rect):
            if not self.triggered:
                self.on_enter()
                self.triggered = True
        else:
            self.triggered = False