from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.enemies.laser import Laser

import pygame

import constants

from windows.hackwindow import HackWindow

from entities.player import Player

class Fusebox():

    def __init__(self, pos: pygame.math.Vector2, laser: Laser):
        self.rect: pygame.Rect = pygame.Rect(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        self.laser: Laser = laser

        self.activated: bool = False
        self.tick_increment: float = 0

        self.window = HackWindow()

    def interect(self, player: Player):
        player_pos: pygame.math.Vector2 = pygame.math.Vector2(player.get_hitbox().center)

        distance: float = player_pos.distance_to((self.rect.centerx, self.rect.centery))
        
        if distance < constants.INTERACT_RANGE:
            self.activated = True # TODO: dont need with minigame
            self.window.active = True
            self.tick_increment = 0 # TODO: figure out how many times we can attemp minigame; might not need to reset here

    def update(self, dt: float):
        self.tick_increment += min(dt, 1 - self.tick_increment)

        if self.tick_increment == 1:
            print("update minigame")
            self.tick_increment = 0
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)