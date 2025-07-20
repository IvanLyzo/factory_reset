import pygame

from constants import *

from core.scene import Scene

from scenes.gameplay import GameplayScene
from scenes.options import OptionsScene

from ui.window import Window
from ui.element import UIElement

class MenuScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.title_window = Window(pygame.Rect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        self.title_window.add_element(60, "Factory Reset", self.game.title_font)

        self.title_window.add_element(120, "Start", self.game.normal_font, callback=self.play)
        self.title_window.add_element(160, "Options", self.game.normal_font, callback=self.options)
        self.title_window.add_element(200, "Quit", self.game.normal_font, callback=game.quit)

        self.title_window.visible = True

    def play(self):
        self.game.change_scene(GameplayScene(self.game))
    
    def options(self):
        self.game.change_scene(OptionsScene(self.game))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.title_window.visible:
                if event.key == pygame.K_UP:
                    self.title_window.switch_options(-1)
                if event.key == pygame.K_DOWN:
                    self.title_window.switch_options(1)

                if event.key == pygame.K_RETURN:
                    self.title_window.select_option()

    def update(self, dt):
        pass  # Nothing to update yet

    def draw(self, screen):
        screen.fill((50, 50, 50))

        self.title_window.draw(screen)
