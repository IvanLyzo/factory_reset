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

from core.gameobject import GameObject

from map.tile import Direction

from entities.enemy import Enemy
from entities.enemies.fusebox import Fusebox
from windows.hackwindow import HackState

# Laser enemy type (inherits Enemy -> GameObject)
class Laser(Enemy):

    def __init__(self, pos: pygame.math.Vector2, catcher_pos: pygame.math.Vector2, fusebox_pos: pygame.math.Vector2, direction: Direction):
        super().__init__(pos, True, 16)  # base_height is 16 because laser is mounted on wall

        # direction laser faces
        self.direction: Direction = direction

        # setup animation fields for laser
        self.animations["active"] = utils.load_animation("enemies/laser/active", 1)
        self.animations["disabled"] = utils.load_animation("enemies/laser/disabled", 1)
        self.animations["deactive"] = utils.load_animation("enemies/laser/deactivate")

        # start with active animation, rotated based on direction
        self.current_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["active"]]

        # catcher object (to prevent laser from firing into wall)
        self.catcher = LaserCatcher(pygame.math.Vector2(catcher_pos.x * constants.VIRTUAL_TILE, catcher_pos.y * constants.VIRTUAL_TILE), direction)

        # beam rect between laser and catcher
        self.beam_rect: pygame.Rect = self.gen_laser()

        # countdown for how often laser damages player
        self.damage_countdown: float = 0

        # fusebox reference
        self.fusebox: Fusebox = Fusebox(fusebox_pos, self)

    # generate laser beam rect between this laser and its catcher
    def gen_laser(self):

        # beam thickness
        thickness: int = int(constants.VIRTUAL_TILE / 8)

        # horizontal laser
        if self.direction.vector.x != 0:
            x: int = self.collision_rect.centerx
            y: int = int(self.collision_rect.centery - thickness / 2)
            width: int = abs(self.catcher.collision_rect.centerx - self.collision_rect.centerx)
            height: int = thickness

            # adjust left-facing beam to start further left
            if self.direction.vector.x < 0:
                x -= width

        # vertical laser
        else:
            x: int = int(self.collision_rect.centerx - thickness / 2)
            y: int = self.collision_rect.centery
            width: int = thickness
            height: int = abs(self.catcher.collision_rect.centery - self.collision_rect.centery)

            # adjust upward beam
            if self.direction.vector.y < 0:
                y -= height

        return pygame.Rect(x, y, width, height)

    # update laser logic
    def update(self, dt: float, game: GameWindow):
        super().update(dt)
        self.catcher.update()
        self.fusebox.update()

        # handle minigame completion and animation transition
        if self.fusebox.window.state == HackState.PASSED:
            if self.current_animation == self.animations["disabled"]:
                return  # already fully deactivated

            # play deactivation animation if not already in it
            if self.current_animation != self.animations["deactive"]:
                self.current_animation = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["deactive"]]
                self.current_frame = 0

            # step through deactivation animation
            elif self.current_frame < len(self.current_animation) - 1:
                self.current_frame += 1

            # switch to disabled animation after deactivation completes
            else:
                self.current_animation = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["disabled"]]
                self.current_frame = 0

            return  # stop beam logic while disabled

        # decrement damage cooldown
        self.damage_countdown -= min(dt, self.damage_countdown)

        # damage player if colliding with beam
        if self.beam_rect.colliderect(game.player.collision_rect) and self.damage_countdown == 0:
            game.player.hit(20)
            game.trigger_alarm()
            self.damage_countdown = 3

        # reset cooldown if no longer colliding
        elif not self.beam_rect.colliderect(game.player.collision_rect):
            self.damage_countdown = 0

    # draw laser
    def draw(self, surface: pygame.Surface):
        img: pygame.Surface = self.current_animation[self.current_frame]
        super().draw(surface, img)

        # only draw beam if still active
        if self.active:
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
        self.animations["idle"] = utils.load_animation("enemies/laser/catcher", 1)
        self.current_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, (self.direction.img_angle + 180) % 360) for frame in self.animations["idle"]]
    
    # update
    def update(self):
        super().update()

    # draw LaserCatcer
    def draw(self, surface: pygame.Surface):
        img: pygame.Surface = self.current_animation[self.current_frame] # get current animation frame
        super().draw(surface, img) # draw frame