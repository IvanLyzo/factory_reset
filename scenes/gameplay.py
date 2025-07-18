import pygame

from core.scene import Scene
from core.level import Level

from entities.player import Player
from entities.enemies.officedrone import OfficeDrone

class GameplayScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.level = Level(1)

        self.player = Player((100, 100))

        self.enemies = []
        self.enemies.append(OfficeDrone((200, 200), [(250, 200), (250, 150), (200, 150), (200, 200)]))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.change_scene(MenuScene(self.game))

        self.player.handle_input(event)

    def update(self, dt):
        self.player.move(self.level.room, dt)

        for enemy in self.enemies:
             enemy.update(dt, self.player)

    def draw(self, screen):
        self.level.draw(screen)
        self.player.draw(screen)

        for enemy in self.enemies:
             enemy.draw(screen)
