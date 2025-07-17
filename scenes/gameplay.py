import pygame

from core.scene import Scene
from core.level import Level
from entities.player import Player

class GameplayScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.current_level = Level(1)

        self.player = Player((100, 100))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.change_scene(MenuScene(self.game))

        self.player.handle_input(event)

    def update(self, dt):
        self.player.move(self.current_level.room, dt)

    def draw(self, screen):
        screen.fill((0, 100, 0))

        self.current_level.draw(screen)

        self.player.draw(screen)
