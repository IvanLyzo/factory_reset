# imports used to delay certain module imports to avoid circular import
from __future__ import annotations
from typing import TYPE_CHECKING

# delayed imports
if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

# normal imports
import pygame

import constants
import utils

from entities.enemy import Enemy

# OfficeDrone enemy type (inherits Enemy -> GameObject)
class OfficeDrone(Enemy):

    def __init__(self, pos: pygame.math.Vector2, targets: list[pygame.math.Vector2]):
        super().__init__(pos, False)

        # setup animation fields for drone (inherited from superclass GameObject)
        self.animations["passive"] = utils.load_animation("enemies/drone/passive")
        self.animations["agro"] = utils.load_animation("enemies/drone/agro")

        self.current_animation: list[pygame.Surface] = self.animations["passive"]

        # speed of movement
        self.speed: int = 50

        # init targets to move to (cycles moving to each target)
        self.targets: list[pygame.math.Vector2] = []
        for target in targets:
            self.targets.append(pygame.math.Vector2(target.x * constants.VIRTUAL_TILE, target.y * constants.VIRTUAL_TILE))
        
        # target index
        self.target_index: int = 0

    # update drone
    def update(self, dt: float, game: GameWindow):
        super().update(dt) # update baseclass

        # switch animation from passive to agro depending on stealth state
        if game.stealth == True:
            self.current_animation = self.animations["passive"]
        else:
            self.current_animation = self.animations["agro"]

        # do not move if inactive
        if self.active == False:
            return

        # set current target
        target: pygame.math.Vector2 = self.targets[self.target_index]

        # set delta
        delta: pygame.math.Vector2 = pygame.math.Vector2()

        # set delta x
        if target.x > self.pos.x:
            delta.x = min(self.speed * dt, target.x - self.pos.x)
        elif target.x < self.pos.x:
            delta.x = -min(self.speed * dt, self.pos.x - target.x)

        # set delta y
        if target.y > self.pos.y:
            delta.y = min(self.speed * dt, target.x - self.pos.y)
        elif target.y < self.pos.y:
            delta.y = -min(self.speed * dt, self.pos.y - target.y)

        # apply delta
        self.move_to(self.pos + delta)

        # switch targets if needed (rotate if spillover)
        if self.pos == self.targets[self.target_index]:
            self.target_index = (self.target_index + 1) % len(self.targets)
        
        # check if "found" player
        body: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        if body.colliderect(game.player.collision_rect):
            game.trigger_alarm() # trigger game alarm

    # draw drone
    def draw(self, surface: pygame.Surface):
        
        # get current frame from current animation
        img: pygame.Surface = self.current_animation[self.current_frame]

        # draw img on surface
        super().draw(surface, img)