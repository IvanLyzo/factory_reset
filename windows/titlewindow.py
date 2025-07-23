from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game

import pygame

import constants

from windows.gamewindow import GameWindow
from windows.optionswindow import OptionsWindow

from ui.menuwindow import MenuWindow

class TitleWindow(MenuWindow):

    def __init__(self, game: Game):
        super().__init__(0)
        
        # reference to main game instance
        self.game: Game = game

        # title text element
        self.add_element(60, "Factory Reset", constants.h1)

        # menu options with callbacks
        self.add_element(120, "Start", constants.p, callback=self.play)
        self.add_element(160, "Quit", constants.p, callback=game.quit)

    # start the game by switching to GameWindow
    def play(self):
        self.game.change_window(GameWindow(self.game))
    
    # open the options menu
    def options(self):
        self.game.change_window(OptionsWindow(self.game))

    def handle_event(self, event: pygame.event.Event):
        # delegate event handling to MenuWindow
        super().handle_event(event)

    def update(self, dt: float):
        pass  # Nothing to update yet

    def draw(self, screen: pygame.Surface):
        super().draw(screen)