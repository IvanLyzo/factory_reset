from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game

import pygame

from windows.gamewindow import GameWindow
from windows.optionswindow import OptionsWindow

from ui.menuwindow import MenuWindow

class TitleWindow(MenuWindow):

    def __init__(self, game: Game):
        super().__init__(0)
        self.game: Game = game

        self.add_element(60, "Factory Reset", self.game.title_font)

        self.add_element(120, "Start", self.game.normal_font, callback=self.play)
        self.add_element(160, "Options", self.game.normal_font, callback=self.options)
        self.add_element(200, "Quit", self.game.normal_font, callback=game.quit)

    def play(self):
        self.game.change_scene(GameWindow(self.game))
    
    def options(self):
        self.game.change_scene(OptionsWindow(self.game))

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

    def update(self, dt: float):
        pass  # Nothing to update yet

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
