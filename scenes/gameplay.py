import pygame

from constants import *

from core.scene import Scene
from core.level import Level

from entities.player import Player

from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret

class GameplayScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.level = Level(1)

        self.player = Player((self.level.player_spawn[0], self.level.player_spawn[1]))

        self.enemies = []
        for enemy in self.level.enemies:
            type = enemy["type"]
            spawn = (enemy["spawn"][0], enemy["spawn"][1])

            if type == "DRONE":
                targets = []
                for target in enemy["targets"]:
                    targets.append((target[0], target[1]))

                self.enemies.append(OfficeDrone(spawn, targets))
            elif type == "TURRET":
                self.enemies.append(Turret((enemy["spawn"][0], enemy["spawn"][1])))

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
        # draw floor (does not affect 3d effect)
        self.level.draw_floor(screen)

        # draw every "3D" object from top to bottom for 3D effect
        tiles = self.level.get_walls()
        drawables = [*tiles, *self.enemies, self.player]

        drawables.sort(key=lambda obj: obj.rect.bottom)
        for obj in drawables:
            obj.draw(screen)
