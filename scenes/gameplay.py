import pygame

import constants
import utils

from core.scene import Scene

from map.level import Level
from map.trigger import Trigger

from entities.player import Player

from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret

from ui.window import Window

class GameplayScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.paused = False
        self.pause_menu = Window((40, 40, 240, 160))
        self.pause_menu.add_element(20, "Paused", self.game.title_font)
        self.pause_menu.add_element(120, "Exit", self.game.normal_font, callback=self.return_main)

        self.death_menu = Window((80, 80, 160, 80))
        self.death_menu.add_element(20, "Game Over", self.game.title_font)
        self.death_menu.add_element(50, "Restart", self.game.normal_font, callback=self.restart)
        self.death_menu.add_element(65, "Quit", self.game.normal_font, callback=self.return_main) # TODO: make fonts more universal (put in constants or utils probably (give them names after HTML for readability))

        self.player = Player((1, 1))
        self.stealth = True

        self.generate_level(1)
        
    def generate_level(self, floor):
        self.level = Level(floor)

        self.player.set_pos((self.level.player_spawn[0], self.level.player_spawn[1]))

        self.generate_room(0)
    
    def generate_room(self, index, door_index=None):
        self.level.load_room(index)

        if self.level.elevator != None:
            self.elevator = Trigger(utils.get_bounds(self.level.elevator["tiles"]), lambda: self.generate_level(self.level.elevator["to_floor"]))
            self.elevator_room = True
        else:
            self.elevator_room = False

        self.doors = self.generate_doors()
        self.enemies = self.generate_enemies()

        if door_index != None:
            door = self.doors.get(door_index)
            door.triggered = True

            self.player.set_pos(((door.rect.center[0] / constants.VIRTUAL_TILE, door.rect.center[1] / constants.VIRTUAL_TILE)))
        
    def generate_doors(self):
        doors = {}

        for door in self.level.doors:
            rect = utils.get_bounds(door["tiles"])
            
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
    
    def restart(self):
        self.game.change_scene(GameplayScene(self.game))
    
    def return_main(self):
        from scenes.menu import MenuScene
        self.game.change_scene(MenuScene(self.game))
    
    def trigger_alarm(self):
        self.stealth = False
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                self.pause_menu.toggle()

            if event.key == pygame.K_UP:
                self.pause_menu.switch_options(-1)
                self.death_menu.switch_options(-1)
            if event.key == pygame.K_DOWN:
                self.pause_menu.switch_options(1)
                self.death_menu.switch_options(1)
            if event.key == pygame.K_RETURN:
                self.pause_menu.select_option()
                self.death_menu.select_option()

            if event.key == pygame.K_SPACE:
                self.player.emp(self.enemies)

    def update(self, dt):
        if self.paused:
            return
        
        if self.player.alive == False:
            self.paused = True
            self.death_menu.visible = True # TODO: change from visible to active for clarity

        self.solids = [*self.level.get_solids(), *[enemy for enemy in self.enemies if not isinstance(enemy, OfficeDrone)], self.player]
        
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        self.player.update(self, dt)

        for door in self.doors.values():
            door.check(self.player)

        if self.elevator_room == True:
            self.elevator.check(self.player)

        for enemy in self.enemies:
            enemy.update(dt, self)

    def draw(self, screen):
        # draw floor (does not affect 3d effect)
        self.level.draw_floor(screen)

        # draw every "3D" object from top to bottom for 3D effect
        objs = sorted(self.solids, key=lambda obj: obj.rect.bottom)
        for obj in objs:
            obj.draw(screen)

        # draw drones (in sky so draw last)
        for enemy in self.enemies:
            if isinstance(enemy, OfficeDrone):
                enemy.draw(screen)

        self.pause_menu.draw(screen)
        self.death_menu.draw(screen)