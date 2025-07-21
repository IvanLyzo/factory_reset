# type: ignore

from __future__ import annotations
import pygame

import constants

class Window:

    def __init__(self, offset: int, parent: Window | None = None):
        # create rect for window
        parent_rect: pygame.Rect = pygame.Rect(0, 0, constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT)
        if parent is not None:
            parent_rect = parent.rect
        self.rect: pygame.Rect = pygame.Rect(parent_rect.left + offset, parent_rect.top + offset, parent_rect.width - 2 * offset, parent_rect.height - 2 * offset)

        self.active: bool = False

    def handle_event(self, event: pygame.event.Event):
        pass  # Override in subclass

    def update(self, dt: float):
        pass  # Override in subclass

    def draw(self, screen: pygame.Surface):
        pass  # Override in subclass