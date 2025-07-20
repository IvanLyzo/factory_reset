import pygame

import constants
import utils

from entities.enemy import Enemy

class Laser(Enemy):

    def __init__(self, pos, catcher_pos, direction):
        super().__init__(pos)

        self.catcher_rect = pygame.Rect(catcher_pos[0] * constants.VIRTUAL_TILE, catcher_pos[1] * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        self.collided = False

        self.direction = direction

        self.animations["fire"] = utils.load_animation("enemies/turret")
        self.current_animation = self.animations["fire"]
        self.catcher_animation = self.animations["fire"]
        self.animation_speed = 125

        match self.direction:
            case "RIGHT":
                angle = 270
                self.laser_rect = pygame.Rect(
                    self.rect.right + constants.VIRTUAL_TILE / 4,
                    self.rect.centery - constants.VIRTUAL_TILE / 8,
                    self.catcher_rect.left - constants.VIRTUAL_TILE / 4 - self.rect.right,
                    constants.VIRTUAL_TILE / 4
                )
            case "DOWN":
                angle = 180
                self.laser_rect = pygame.Rect(
                    self.rect.centerx - constants.VIRTUAL_TILE / 8,
                    self.rect.bottom + constants.VIRTUAL_TILE / 4,
                    constants.VIRTUAL_TILE / 4,
                    self.catcher_rect.top - constants.VIRTUAL_TILE / 4 - self.rect.bottom
                )
            case "LEFT":
                angle = 90
                self.laser_rect = pygame.Rect(
                    self.catcher_rect.right + constants.VIRTUAL_TILE / 4,
                    self.rect.centery - constants.VIRTUAL_TILE / 8,
                    self.rect.left - self.catcher_rect.right - constants.VIRTUAL_TILE / 4,
                    constants.VIRTUAL_TILE / 4
                )
            case "UP":
                angle = 0
                self.laser_rect = pygame.Rect(
                    self.rect.centerx - constants.VIRTUAL_TILE / 8,
                    self.catcher_rect.centery,
                    constants.VIRTUAL_TILE / 4,
                    self.rect.centery - self.catcher_rect.centery
                )

        self.current_animation = [pygame.transform.rotate(frame, angle) for frame in self.current_animation]
        self.catcher_animation = [pygame.transform.rotate(frame, (angle + 180) % 360) for frame in self.catcher_animation]

        # TODO: connect to "fusebox" to allow disabling

    def update(self, dt, game):
        super().update(dt)

        if self.laser_rect.colliderect(game.player.get_hitbox()) and not self.collided:
            game.player.hit(50)
            game.trigger_alarm()

            self.collided = True
        elif not self.laser_rect.colliderect(game.player.get_hitbox()):
            self.collided = False

    def draw(self, surface):
        laser_img = self.current_animation[self.current_frame]
        catcher_img = self.catcher_animation[self.current_frame]
        
        surface.blit(laser_img, (self.rect.x, self.rect.y))
        surface.blit(catcher_img, (self.catcher_rect.x, self.catcher_rect.y))

        pygame.draw.rect(surface, (200, 10, 10), self.laser_rect)