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

from core.gameobject import GameObject

from map.tile import Direction

from entities.enemy import Enemy
from entities.enemies.fusebox import Fusebox

# Laser enemy type (inherits Enemy -> GameObject)
class Laser(Enemy):

    def __init__(self, pos: pygame.math.Vector2, catcher_pos: pygame.math.Vector2, fusebox_pos: pygame.math.Vector2, direction: Direction):
        super().__init__(pos, True, 16) # base_height is 16 because - like turret - laser is on the wall

        # direction turret faces
        self.direction: Direction = direction

        # TODO: art: art for catcher and laser
        self.animations["fire"] = utils.load_animation("enemies/turret")
        self.current_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["fire"]]

        # catcher enemy (laser cant just shoot into the wall - think of all the company expenses it would take to fix that!!!)
        self.catcher = LaserCatcher(pygame.math.Vector2(catcher_pos.x * constants.VIRTUAL_TILE, catcher_pos.y * constants.VIRTUAL_TILE), direction)

        # beam rect between laser and catcher
        self.beam_rect: pygame.Rect = self.gen_laser()

        # countdown until next damage tick
        self.damage_countdown: float = 0

        # fusebox reference (for disabling laser)
        self.fusebox: Fusebox = Fusebox(fusebox_pos, self)

    # dynamically generate laser beam between laser and catcher (no matter where either are)
    def gen_laser(self):

        # thickness of laser beam (likely wont be float so cast is useless but uncasted division is scary!!!)
        thickness: int = int(constants.VIRTUAL_TILE / 4)

        # horizontal laser
        if self.direction.vector.x != 0:
            
            # laser positions
            x: int = self.collision_rect.centerx
            y: int = int(self.collision_rect.centery - thickness / 2) # halved to keep centered

            # laser dimensions
            width: int = abs(self.catcher.collision_rect.centerx - self.collision_rect.centerx) # absolute distance between laser and catcher (no need to cast to int since rects can't hold floats)
            height: int = thickness
            
            # adjust x for left-facing laser (x has to be topLEFT for drawing)
            if self.direction.vector.x < 0:
                x -= width
        
        # vertical laser
        else:

            # laser pos
            x: int = int(self.collision_rect.centerx - thickness / 2) # halved to keep centered (on x axis this time)
            y: int = self.collision_rect.centery

            # laser dimensions
            width: int = thickness
            height:int = abs(self.catcher.collision_rect.centery - self.collision_rect.centery) # absolute distance between laser and catcher
            
            # adjust y for up-facing laser (y has to be TOPleft for drawing)
            if self.direction.vector.y < 0:
                y -= height

        # return rect
        return pygame.Rect(x, y, width, height)

    # update laser enemy
    def update(self, dt: float, game: GameWindow):

        # if fusebox was activated, tell gamewindow to start minigame
        if self.fusebox.activated:
            game.start_minigame(self.fusebox)

        # update superclass
        super().update(dt)

        # update catcher
        self.catcher.update()

        # update damage countdown (ensuring countdown never goes negative)
        self.damage_countdown -= min(dt, self.damage_countdown)

        # if beam collides with player 
        if self.beam_rect.colliderect(game.player.collision_rect) and self.damage_countdown == 0:
            game.player.hit(20) # hit player (every 3 seconds)
            game.trigger_alarm() # trigger alarm

            self.damage_countdown = 3 # reset damage_countdown to 3 seconds
    
    # draw laser
    def draw(self, surface: pygame.Surface):
        img: pygame.Surface = self.current_animation[self.current_frame]
        super().draw(surface, img)

        pygame.draw.rect(surface, (200, 10, 10), self.beam_rect)

        # draw fusebox
        self.fusebox.draw(surface)

# small LaserCatcher class extending game object
class LaserCatcher(GameObject):

    def __init__(self, pos: pygame.math.Vector2, direction: Direction):
        super().__init__(pos, True, 16)

        # direction facing
        self.direction: Direction = direction

        # setup animation fields for LaserCatcher (inherited from superclass GameObject)
        self.animations["fire"] = utils.load_animation("enemies/turret")
        self.current_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, (self.direction.img_angle + 180) % 360) for frame in self.animations["fire"]]
    
    # draw LaserCatcer
    def draw(self, surface: pygame.Surface):
        img: pygame.Surface = self.current_animation[self.current_frame] # get current animation frame
        super().draw(surface, img) # draw frame