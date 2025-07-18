import pygame

from core.scene import Scene
from core.level import Level

from entities.player import Player

from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret

class GameplayScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.level = Level(1)

        self.player = Player((100, 100))

        self.enemies = []
        self.enemies.append(OfficeDrone((200, 200), [(250, 200), (250, 150), (200, 150), (200, 200)]))
        self.enemies.append(Turret((100, 200)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.change_scene(MenuScene(self.game))

            if event.key == pygame.K_SPACE:
                self.player.emp(self.enemies)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        self.player.move(self.level.room, dt)

        for enemy in self.enemies:
            enemy.update(dt, self.player)

    def draw(self, screen):
        self.level.draw(screen)
        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)
