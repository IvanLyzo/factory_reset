from __future__ import annotations
import pygame

import constants

class Window:

    def __init__(self, offset: int, parent: Window | None = None, custom_pos: pygame.Rect | None = None):

        # get parent rect (use screen if None)
        parent_rect: pygame.Rect = pygame.Rect(0, 0, constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT)
        if parent is not None:
            parent_rect = parent.rect
        
        # if set custom size, follow that
        if custom_pos is not None:
            self.rect: pygame.Rect = pygame.Rect(parent_rect.left + custom_pos.x, parent_rect.top + custom_pos.y, custom_pos.width, custom_pos.height)

        # else if just offset, create centered window
        else:
            self.rect: pygame.Rect = pygame.Rect(parent_rect.left + offset, parent_rect.top + offset, parent_rect.width - 2 * offset, parent_rect.height - 2 * offset)

        self.active: bool = False

    def handle_event(self, event: pygame.event.Event):
        pass  # Override in subclass

    def update(self, dt: float):
        pass  # Override in subclass

    def draw(self, screen: pygame.Surface):
        pass  # Override in subclass