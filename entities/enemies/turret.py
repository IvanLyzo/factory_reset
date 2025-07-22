# imports used to delay certain module imports to avoid ciruclar import
from __future__ import annotations
from typing import TYPE_CHECKING

# delayed imports
if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

# normal imports
import pygame

import constants
import utils

from map.tile import Direction

from entities.enemy import Enemy

# Turret enemy type (inherits Enemy -> GameObject)
class Turret(Enemy):

    def __init__(self, pos: pygame.math.Vector2, direction: Direction):
        super().__init__(pos, True, 16) # base_height is 16 because of turret orientation on wall making it entirely collidable

        # direction turret faces and fires (enum)
        self.direction: Direction = direction

        # setup animation fields for Turret (inherited from superclass GameObject)
        self.animations["fire"] = utils.load_animation("enemies/turret")
        self.current_animation = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["fire"]]

        # list of fired pellets ("bullets")
        self.pellets: list[Pellet] = []

        # flag for if already show this animation frame (shooting tied to animation)
        self.shot_frame: bool = False

    # update turret
    def update(self, dt: float, game: GameWindow):

        # turret is inactive completely (no animation even) if in stealth state
        if game.stealth == True:
            return

        # update baseclass
        super().update(dt)

        # update all fired pellets
        for bullet in self.pellets:
            bullet.update(dt, game)

        # append new bullet if time to shoot
        if self.current_frame == 1 and not self.shot_frame and self.active:
            self.pellets.append(Pellet(self, pygame.math.Vector2(self.collision_rect.centerx, self.collision_rect.centery)))
            self.shot_frame = True
        
        # reset shot flag for next animation loop
        if self.current_frame == 2:
            self.shot_frame = False

    # draw turret and pellets
    def draw(self, surface: pygame.Surface):

        # get current animation frame from current animation
        img: pygame.Surface = self.current_animation[self.current_frame]

        # draw turret as game object
        super().draw(surface, img)

        # draw pellets
        for pellet in self.pellets:
            pellet.draw(surface)

# small pellet class (shares some game object traits but not enough to make it a game object; no animation for example)
class Pellet:

    def __init__(self, turret: Turret, pos: pygame.math.Vector2):

        # keep reference to parent turret
        self.turret: Turret = turret

        # size of pellet
        self.size: int = int(constants.VIRTUAL_TILE / 8)
        
        # speed
        self.speed = 75

        # set rect and direction
        self.rect = pygame.Rect(pos.x - self.size / 2, pos.y - self.size / 2, self.size, self.size)
        self.dir = turret.direction.vector

    # update pellet
    def update(self, dt: float, game: GameWindow):

        # update position
        center = pygame.Vector2(self.rect.center)
        center += self.dir * self.speed * dt

        # use vector2 center, but assign expected and rounded tuple[int, int]
        self.rect.center = (round(center.x), round(center.y))

        # check for player collision with entire player box (bullets don't have to hit "legs")
        player_box = pygame.Rect(game.player.pos.x, game.player.pos.y, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)

        if self.rect.colliderect(player_box):
            self.turret.pellets.remove(self) # remove pellet
            game.player.hit(10) # notify player of collision

        # if went out of screen, remove pellet (unlikely because of surrounding walls but technically possible through doors)
        if self.rect.bottom < 0 or self.rect.top > constants.VIRTUAL_HEIGHT or self.rect.right < 0 or self.rect.left > constants.VIRTUAL_WIDTH:
            self.turret.pellets.remove(self)

        # check for collision with solid tiles and remove
        for obj in game.floor.get_solids():

            # can safely check collision rect because guaranteed by get_solids() (even though technically could raise erorr)
            if self.rect.colliderect(obj.collision_rect):
                self.turret.pellets.remove(self)
    
    # draw pellet as small white square (i'm not adding graphics for a 4-pixel square)
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)