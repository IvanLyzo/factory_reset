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
from entities.enemies.laser import Laser
from entities.enemies.fusebox import Fusebox

from ui.menuwindow import MenuWindow
from ui.window import Window

from windows.hackwindow import HackWindow, HackState
        
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

        # Reference to main game instance
        self.game: Game = game

        # Current game state (play, pause, minigame, ended)
        self.game_state: GameState = GameState.PLAY

        # Pause menu UI window setup
        self.pause_menu: MenuWindow = MenuWindow(40, parent=self)
        self.pause_menu.add_element(20, "Paused", constants.h1)
        self.pause_menu.add_element(120, "Exit", constants.p, callback=self.return_main)

        # Death menu UI window setup
        self.death_menu: MenuWindow = MenuWindow(40, parent=self)
        self.death_menu.add_element(20, "Game Over", constants.h1)
        self.death_menu.add_element(80, "Restart", constants.p, callback=self.restart)
        self.death_menu.add_element(100, "Quit", constants.p, callback=self.return_main)

        # Player instance, positioned initially at (1, 1) grid coordinate
        self.player: Player = Player(pygame.math.Vector2(1, 1))

        # Flag indicating if stealth mode is active
        self.stealth: bool = True

        # Optional minigame UI window
        self.minigame: HackWindow | None = None
        
        # Track current floor number and generate floor 2 at start
        self.current_floor: int = 0
        self.gen_floor(2)
        
    def gen_floor(self, floor: int):
        # Update current floor index
        self.current_floor = floor

        # Create Floor object for the given floor number
        self.floor: Floor = Floor(self, floor)

        # Move player to spawn point on the floor, scaled by tile size
        self.player.move_to(pygame.math.Vector2(self.floor.player_spawn.x * constants.VIRTUAL_TILE, self.floor.player_spawn.y * constants.VIRTUAL_TILE))
    
    def switch_room(self, room_index: int, door_index: int | None = None):
        # Load a new room in the current floor by index
        self.floor.load_room(self, room_index)

        if door_index is not None:
            # Mark the door trigger as triggered to avoid immediate re-trigger
            door: Trigger | None = self.floor.doors.get(door_index)
            self.floor.doors.get(door_index).triggered = True

            # Move player to center of the door's rectangle
            self.player.move_to(pygame.math.Vector2(door.rect.left, door.rect.top))
    
    def restart(self):
        # Restart game by creating a fresh GameWindow instance
        self.game.change_window(GameWindow(self.game))
    
    def return_main(self):
        # Return to the main title window
        self.game.change_window(TitleWindow(self.game))
    
    def trigger_alarm(self):
        # Disable stealth mode (trigger alarm state)
        self.stealth = False
    
    def start_minigame(self, window: HackWindow):
        # Switch state to minigame and set current minigame window
        self.game_state = GameState.MINIGAME
        self.minigame = window
    
    def handle_event(self, event: pygame.event.Event):
        # Only handle keyboard keydown events
        if event.type != pygame.KEYDOWN:
            return

        match self.game_state:
            case GameState.PLAY:
                # Escape key toggles pause menu
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu.toggle()

                # 'E' key interaction with fuseboxes for lasers
                if event.key == pygame.K_e:
                    for enemy in self.floor.enemies:
                        if isinstance(enemy, Laser):
                            enemy.fusebox.interact(self)

                # Space key triggers EMP ability for player
                if event.key == pygame.K_SPACE:
                    self.player.emp(self.floor.enemies)
            
            case GameState.PAUSED:
                # Pass input to pause menu UI
                self.pause_menu.handle_event(event)

            case GameState.ENDED:
                # Pass input to death menu UI
                self.death_menu.handle_event(event)

            case GameState.MINIGAME:
                # Pass input to current minigame UI window
                if self.minigame is not None:
                    self.minigame.handle_event(event)

    def update(self, dt: float):
        match self.game_state:
            case GameState.PLAY:
                # If player is inactive, game is ended and death menu active
                if not self.player.active:
                    self.game_state = GameState.ENDED
                    self.death_menu.active = True

                # If player died, regenerate floor and reset state
                if self.player.died:
                    self.gen_floor(self.current_floor)
                    self.stealth = True
                    self.player.died = False

                # Build list of solid objects for collision and draw order
                self.solids: list[GameObject | pygame.Rect] = [
                    self.player,  # player object
                    *self.floor.get_solids(),  # solid tiles
                    *[enemy for enemy in self.floor.enemies if not isinstance(enemy, OfficeDrone)],  # enemies except drones
                    *[laser.catcher for laser in self.floor.enemies if isinstance(laser, Laser)],  # laser catchers
                    *[laser.fusebox for laser in self.floor.enemies if isinstance(laser, Laser)]  # laser fuseboxes
                ]
                
                # Get current key states and handle player input
                keys: list[bool] = pygame.key.get_pressed()
                self.player.handle_input(keys)

                # Update player object
                self.player.update(self, dt)

                # Check all door triggers against player
                for door in self.floor.doors.values():
                    door.check(self.player)

                # Check elevator trigger if room has one
                if self.floor.elevator_room:
                    self.floor.elevator.check(self.player)

                # Update all enemies
                for enemy in self.floor.enemies:
                    enemy.update(dt, self)

            case GameState.MINIGAME:
                if self.minigame is not None:
                    # Update minigame window
                    self.minigame.update(dt)

                    # After minigame ends, return to play + trigger alarm on failure
                    if self.minigame.state is not HackState.IN_PROGRESS:
                        self.game_state = GameState.PLAY
                        
                        if self.minigame.state is HackState.FAILED:
                            self.trigger_alarm()

    def draw(self, screen: pygame.Surface):
        # Draw floor tiles (no 3D effect)
        self.floor.draw_floor(screen)

        # Draw all solid objects sorted by collision bottom for 3D layering
        objs: list[GameObject | pygame.Rect] = sorted(self.solids, key=lambda obj: obj.collision_rect.bottom)
        for obj in objs:
            obj.draw(screen)

        # Draw flying drones last (appear in sky, always on top)
        for enemy in self.floor.enemies:
            if isinstance(enemy, OfficeDrone):
                enemy.draw(screen)
        
        # Draw player's UI window
        self.player.player_ui.draw(screen)

        # Draw UI windows based on game state
        match self.game_state:
            case GameState.PAUSED:
                self.pause_menu.draw(screen)

            case GameState.ENDED:
                self.death_menu.draw(screen)
        
            case GameState.MINIGAME:
                if self.minigame is not None:
                    self.minigame.draw(screen)