from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

import pygame

import constants
import utils

from map.tile import Direction

from entities.enemy import Enemy
from entities.enemies.fusebox import Fusebox

class Laser(Enemy):

    def __init__(self, pos: pygame.math.Vector2, catcher_pos: pygame.math.Vector2, fusebox_pos: pygame.math.Vector2, direction: Direction):
        super().__init__(pos)

        self.direction: Direction = direction
        print(catcher_pos)
        self.catcher_rect: pygame.Rect = pygame.Rect(catcher_pos.x * constants.VIRTUAL_TILE, catcher_pos.y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        self.laser_rect: pygame.Rect = self.gen_laser()
        self.collided: bool = False

        # TODO: art: art art for catcher and laser
        self.animations["fire"] = utils.load_animation("enemies/turret")

        self.current_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["fire"]]
        self.catcher_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, (self.direction.img_angle + 180) % 360) for frame in self.animations["fire"]]

        self.fusebox: Fusebox = Fusebox(fusebox_pos, self)

    def gen_laser(self):
        vec: pygame.math.Vector2 = self.direction.vector
        thickness: int = int(constants.VIRTUAL_TILE / 4)

        # horizontal laser
        if vec.x != 0:
            # laser pos
            x = self.rect.centerx
            y = self.rect.centery - thickness / 2

            # laser dimensions
            width = abs(self.catcher_rect.centerx - self.rect.centerx)
            height = thickness
            
            # adjust x for left-facing laser (x has to be left for drawing)
            if vec.x < 0:
                x -= width
        
        # vertical laser
        else:
            # laser pos
            x = self.rect.centerx - thickness / 2
            y = self.rect.centery

            # laser dimensions
            width = thickness
            height = abs(self.catcher_rect.centery - self.rect.centery)
            
            # adjust y for up-facing laser (y has to be top for drawing)
            if vec.y < 0:
                y -= height

        return pygame.Rect(x, y, width, height)

    def update(self, dt: float, game: GameWindow):
        if self.fusebox.activated:
            game.start_minigame(self.fusebox)

        super().update(dt)

        if self.laser_rect.colliderect(game.player.get_hitbox()) and not self.collided:
            game.player.hit(50)
            game.trigger_alarm()

            self.collided = True
        elif not self.laser_rect.colliderect(game.player.get_hitbox()):
            self.collided = False

    def draw(self, surface: pygame.Surface):
        laser_img: pygame.Surface = self.current_animation[self.current_frame]
        catcher_img: pygame.Surface = self.catcher_animation[self.current_frame]
        
        surface.blit(laser_img, self.rect.topleft)
        surface.blit(catcher_img, self.catcher_rect.topleft)

        pygame.draw.rect(surface, (200, 10, 10), self.laser_rect)

        # draw fusebox
        self.fusebox.draw(surface)