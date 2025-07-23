from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game

import pygame

from ui.menuwindow import MenuWindow

class OptionsWindow(MenuWindow):

    def __init__(self, game: Game):
        # Store reference to the main game instance
        self.game: Game = game

        # Call MenuWindow constructor with default offset and no parent/custom position
        super().__init__(0)

    def handle_event(self, event: pygame.event.Event):
        # Override to handle events specific to the options window
        pass

    def update(self, dt: float):
        # Override to update options window logic each frame
        pass

    def draw(self, screen: pygame.Surface):
        # Override to draw options window contents
        pass