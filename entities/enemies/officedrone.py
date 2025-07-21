from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

import pygame

import constants
import utils

from entities.enemy import Enemy

class OfficeDrone(Enemy):

    def __init__(self, pos: pygame.math.Vector2, targets: list[pygame.math.Vector2]):
        super().__init__(pos)

        self.animations["idle"] = utils.load_animation("player/idle")
        self.current_animation: list[pygame.Surface] = self.animations["idle"]

        self.speed: int = 50

        self.targets: list[pygame.math.Vector2] = []
        for target in targets:
            self.targets.append((target.x * constants.VIRTUAL_TILE, target.y * constants.VIRTUAL_TILE))
        self.target_index: int = 0

    def update(self, dt: float, game: GameWindow):
        super().update(dt)

        if self.active == False:
            return

        # move to current target
        target: pygame.math.Vector2 = self.targets[self.target_index]
        if target[0] > self.rect.x:
            self.rect.x += min(self.speed * dt, target[0] - self.rect.x)
        elif target[0] < self.rect.x:
            self.rect.x -= min(self.speed * dt, self.rect.x - target[0])

        if target[1] > self.rect.y:
            self.rect.y += min(self.speed * dt, target[1] - self.rect.y)
        elif target[1] < self.rect.y:
            self.rect.y -= min(self.speed * dt, self.rect.y - target[1])

        # switch targets if needed
        if self.rect.topleft == self.targets[self.target_index]:
            self.target_index = (self.target_index + 1) % len(self.targets)
        
        # check if "found" player
        if self.rect.colliderect(game.player.get_hitbox()):
            game.trigger_alarm()

    def disable(self, time: float):
        super().disable(time)
    
    def draw(self, surface: pygame.Surface):
        img: pygame.Surface = self.current_animation[self.current_frame]

        super().draw(surface, img)