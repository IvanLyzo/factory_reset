from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game

import pygame

from ui.menuwindow import MenuWindow

class OptionsWindow(MenuWindow):

    def __init__(self, game: Game):
        self.game: Game = game
        pass

    def handle_event(self, event: pygame.event.Event):
        pass  # Override in subclass

    def update(self, dt: float):
        pass  # Override in subclass

    def draw(self, screen: float):
        pass  # Override in subclass