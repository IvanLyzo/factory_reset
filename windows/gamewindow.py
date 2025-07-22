from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game
    from windows.titlewindow import TitleWindow

import pygame
from enum import Enum

import constants

from core.gameobject import GameObject

from map.floor import Floor
from map.trigger import Trigger

from entities.player import Player

from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret
from entities.enemies.laser import Laser
from entities.enemies.fusebox import Fusebox

from ui.menuwindow import MenuWindow
from ui.window import Window
        
class GameState(Enum):
    PLAY = (0, False)
    PAUSED = (1, True)
    MINIGAME = (2, True)
    ENDED = (3, True)

    def __init__(self, id: int, paused: bool):
        self.id: int = id
        self.paused: bool = paused

class GameWindow(Window):

    def __init__(self, game: Game):
        super().__init__(0)
        self.game: Game = game
        self.game_state: GameState = GameState.PLAY

        self.pause_menu: MenuWindow = MenuWindow(40, parent=self)
        self.pause_menu.add_element(20, "Paused", self.game.title_font)
        self.pause_menu.add_element(120, "Exit", self.game.normal_font, callback=self.return_main)

        self.death_menu: MenuWindow = MenuWindow(80, parent=self)
        self.death_menu.add_element(20, "Game Over", self.game.title_font)
        self.death_menu.add_element(50, "Restart", self.game.normal_font, callback=self.restart)
        self.death_menu.add_element(65, "Quit", self.game.normal_font, callback=self.return_main) # TODO: make fonts more universal (put in constants or utils probably (give them names after HTML for readability))

        self.player: Player = Player(pygame.math.Vector2(1, 1))
        self.stealth: bool = True

        self.active_fusebox: Fusebox | None = None
        
        self.current_floor = 0
        self.gen_floor(2)
        
    def gen_floor(self, floor: int):
        self.current_floor = floor
        self.floor: Floor = Floor(self, floor)

        self.player.move_to(pygame.math.Vector2(self.floor.player_spawn.x * constants.VIRTUAL_TILE, self.floor.player_spawn.y * constants.VIRTUAL_TILE))
    
    def switch_room(self, room_index: int, door_index: int | None = None):
        self.floor.load_room(self, room_index)

        if door_index != None:
            door: Trigger = self.floor.doors.get(door_index)
            door.triggered = True

            self.player.move_to(pygame.math.Vector2(door.rect.centerx, door.rect.centery))
    
    def restart(self):
        self.game.change_scene(GameWindow(self.game))
    
    def return_main(self):
        self.game.change_scene(TitleWindow(self.game))
    
    def trigger_alarm(self):
        self.stealth = False
    
    def start_minigame(self, fusebox: Fusebox):
        self.game_state = GameState.MINIGAME
        self.active_fusebox = fusebox
    
    def handle_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return

        match self.game_state:
            case GameState.PLAY:
                if event.key == pygame.K_ESCAPE:
                    self.pausedself.paused
                    self.pause_menu.toggle()

                if event.key == pygame.K_e:
                    for enemy in self.floor.enemies:
                        if isinstance(enemy, Laser):
                            enemy.fusebox.interect(self)

                if event.key == pygame.K_SPACE:
                    self.player.emp(self.floor.enemies)
            
            # TODO: remove active checks on menus (guaranteed active)
            case GameState.PAUSED:
                if event.key == pygame.K_UP:
                    self.pause_menu.switch_options(-1)
                    self.death_menu.switch_options(-1)
                if event.key == pygame.K_DOWN:
                    self.pause_menu.switch_options(1)
                    self.death_menu.switch_options(1)
                if event.key == pygame.K_RETURN:
                    self.pause_menu.select_option()
                    self.death_menu.select_option()

            case GameState.ENDED:
                if event.key == pygame.K_UP:
                    self.pause_menu.switch_options(-1)
                    self.death_menu.switch_options(-1)
                if event.key == pygame.K_DOWN:
                    self.pause_menu.switch_options(1)
                    self.death_menu.switch_options(1)
                if event.key == pygame.K_RETURN:
                    self.pause_menu.select_option()
                    self.death_menu.select_option()

            case GameState.MINIGAME:
                # process minigame input
                pass

    def update(self, dt: float):
        match self.game_state:
            case GameState.MINIGAME:
                self.active_fusebox.update(dt)

            case GameState.PLAY:
                if self.player.active == False:
                    self.game_state = GameState.ENDED
                    self.death_menu.active = True

                if self.player.died == True:
                    self.gen_floor(self.current_floor)
                    self.stealth = True

                    self.player.died = False

                self.solids: list[GameObject | pygame.Rect] = [
                    self.player, # player
                    *self.floor.get_solids(), # solid tiles
                    *[enemy for enemy in self.floor.enemies if not isinstance(enemy, OfficeDrone)], # enemies excluding drones
                    *[laser.catcher for laser in self.floor.enemies if isinstance(laser, Laser)] # catchers of all lasers
                    ]
                
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys)

                self.player.update(self, dt)

                for door in self.floor.doors.values():
                    door.check(self.player)

                if self.floor.elevator_room == True:
                    self.floor.elevator.check(self.player)

                for enemy in self.floor.enemies:
                    enemy.update(dt, self)

    def draw(self, screen: pygame.Surface):
        # draw floor (does not affect 3d effect)
        self.floor.draw_floor(screen)

        # draw every "3D" object from top to bottom for 3D effect
        objs = sorted(self.solids, key=lambda obj: obj.collision_rect.bottom)
        for obj in objs:
            obj.draw(screen)

        # draw drones (in sky so draw last)
        for enemy in self.floor.enemies:
            if isinstance(enemy, OfficeDrone):
                enemy.draw(screen)

        match self.game_state:
            case GameState.PAUSED:
                self.pause_menu.draw(screen)

            case GameState.ENDED:
                self.death_menu.draw(screen)
        
            case GameState.MINIGAME:
                self.active_fusebox.window.draw(screen)