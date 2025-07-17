from constants import *

from core.scene import Scene

from scenes.gameplay import GameplayScene
from scenes.options import OptionsScene

from ui.button import Button
from ui.text import Text

class MenuScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.title = Text((VIRTUAL_WIDTH / 2, 48), "Factory Reset", self.game.title_font)

        self.buttons = []
        self.buttons.append(Button((VIRTUAL_WIDTH / 2, 120), "Start", self.game.normal_font, callback=self.play))
        self.buttons.append(Button((VIRTUAL_WIDTH / 2, 160), "Options", self.game.normal_font, callback=self.options))
        self.buttons.append(Button((VIRTUAL_WIDTH / 2, 200), "Quit", self.game.normal_font, callback=game.quit))
        
    def handle_event(self, event):
        for button in self.buttons:
            button.handle_click(event)

    def play(self):
        self.game.change_scene(GameplayScene(self.game))
    
    def options(self):
        self.game.change_scene(OptionsScene(self.game))

    def update(self, dt):
        pass  # Nothing to update yet

    def draw(self, screen):
        screen.fill((50, 50, 50))

        self.title.draw(screen)

        for button in self.buttons:
            button.draw(screen)
