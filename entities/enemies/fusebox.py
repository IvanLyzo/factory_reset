from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.enemies.laser import Laser
    from windows.gamewindow import GameWindow

import pygame

import constants

from windows.hackwindow import HackWindow

class Fusebox():

    def __init__(self, pos: pygame.math.Vector2, laser: Laser):
        self.rect: pygame.Rect = pygame.Rect(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        self.laser: Laser = laser

        self.activated: bool = False
        self.tick_increment: float = 0

        self.window: HackWindow = HackWindow()

    def interect(self, game: GameWindow):
        player_pos: pygame.math.Vector2 = pygame.math.Vector2(game.player.hitbox().center)

        distance: float = player_pos.distance_to((self.rect.centerx, self.rect.centery))
        
        if distance < constants.INTERACT_RANGE and game.stealth == True:
            self.activated = True
            self.window.active = True

    def update(self, dt: float):
        self.tick_increment += min(dt, 1 - self.tick_increment)

        if self.tick_increment == 1:
            print("update minigame")
            self.tick_increment = 0
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)