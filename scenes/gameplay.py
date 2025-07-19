import pygame

from constants import *
from utils import *

from core.scene import Scene

from map.level import Level
from map.triggers.trigger import Trigger
from map.triggers.door import Door

from entities.player import Player

from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret

class GameplayScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.level = Level(1)
        self.generate_room(0)
        
    def generate_room(self, index, door_index=None):
        self.level.load_room(index)

        self.doors = self.generate_doors()

        if door_index == None:
            self.player = Player((1, 1))
        else:
            door = self.doors.get(door_index)
            door.triggered = True
            self.player = Player((door.rect.center[0] / VIRTUAL_TILE, door.rect.center[1] / VIRTUAL_TILE))
            # figure out
        
        self.enemies = self.generate_enemies()
    
    def generate_doors(self):
        doors = {}

        for door in self.level.doors:
            rect = get_bounds(door["tiles"])
            
            id = door["id"]
            to_room = door["to_room"]

            doors[id] = Trigger(rect, lambda: self.generate_room(to_room, id))

        return doors

    def generate_enemies(self):
        enemies = []

        for enemy in self.level.enemies:
            type = enemy["type"]
            spawn = (enemy["spawn"][0], enemy["spawn"][1])

            if type == "DRONE":
                targets = []
                for target in enemy["targets"]:
                    targets.append((target[0], target[1]))
                enemies.append(OfficeDrone(spawn, targets))
            
            elif type == "TURRET":
                enemies.append(Turret(spawn, enemy["direction"]))
        
        return enemies
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.change_scene(MenuScene(self.game))

            # temp test
            if event.key == pygame.K_q:
                self.generate_room(1)

            if event.key == pygame.K_SPACE:
                self.player.emp(self.enemies)

    def update(self, dt):
        self.solids = [*self.level.get_walls(), *self.enemies, self.player]
        
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        no_player = list(filter(lambda x: x != self.player, self.solids))
        self.player.move(no_player, dt)

        for door in self.doors.values():
            door.check(self.player)

        for enemy in self.enemies:
            enemy.update(dt, self.player)

    def draw(self, screen):
        # draw floor (does not affect 3d effect)
        self.level.draw_floor(screen)

        # draw every "3D" object from top to bottom for 3D effect
        objs = sorted(self.solids, key=lambda obj: obj.rect.bottom)
        for obj in objs:
            obj.draw(screen)
