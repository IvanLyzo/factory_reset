from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

import pygame

import constants
import utils

from map.tile import Direction

from entities.enemy import Enemy

class Turret(Enemy):

    def __init__(self, pos: pygame.math.Vector2, direction: Direction):
        super().__init__(pos)

        self.direction: Direction = direction

        self.animations["fire"] = utils.load_animation("enemies/turret")
        self.current_animation = [pygame.transform.rotate(frame, self.direction.img_angle) for frame in self.animations["fire"]]

        self.pellets: list[Pellet] = []
        self.shot_frame: bool = False

    def update(self, dt: float, game: GameWindow):
        if game.stealth == True:
            return

        super().update(dt)

        for bullet in self.pellets:
            bullet.update(dt, game)

        if self.current_frame == 1 and not self.shot_frame and self.active:
            self.shoot()
            self.shot_frame = True
        
        if self.current_frame == 2:
            self.shot_frame = False

    def shoot(self):
        self.pellets.append(Pellet(self, pygame.math.Vector2(self.rect.centerx, self.rect.centery)))
    
    def remove_pellet(self, pellet: Pellet):
        self.pellets.remove(pellet)
    
    def draw(self, surface: pygame.Surface):
        img: pygame.Surface = self.current_animation[self.current_frame]

        super().draw(surface, img)

        for pellet in self.pellets:
            pellet.draw(surface)

class Pellet:

    def __init__(self, turret: Turret, pos: pygame.math.Vector2):
        self.turret: Turret = turret

        self.size: int = int(constants.VIRTUAL_TILE / 8)

        self.speed = 60

        self.rect = pygame.Rect(pos.x - self.size / 2, pos.y - self.size / 2, self.size, self.size)
        self.dir = turret.direction.vector

    def update(self, dt: float, game: GameWindow):
        center = pygame.Vector2(self.rect.center)
        center += self.dir * self.speed * dt

        self.rect.center = (round(center.x), round(center.y))

        if self.rect.colliderect(game.player.get_hitbox()):
            self.turret.remove_pellet(self)

            game.player.hit(10)
            game.trigger_alarm()

        if self.rect.bottom < 0 or self.rect.top > constants.VIRTUAL_HEIGHT or self.rect.right < 0 or self.rect.left > constants.VIRTUAL_WIDTH:
            self.turret.remove_pellet(self)

        for obj in game.floor.get_solids():
            if self.rect.colliderect(obj.rect):
                self.turret.remove_pellet(self)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)