import pygame

import constants
import utils

from entities.enemy import Enemy

class Turret(Enemy):

    def __init__(self, pos, direction):
        super().__init__(pos)

        self.direction = direction

        self.bullets = []
        self.shot_frame = False

        self.animations["fire"] = utils.load_animation("enemies/turret")
        self.current_animation = self.animations["fire"]
        self.animation_speed = 125

        angle = 0
        match self.direction:
            case "RIGHT":
                angle = 270
            case "DOWN":
                angle = 180
            case "LEFT":
                angle = 90
        self.current_animation = [pygame.transform.rotate(frame, angle) for frame in self.current_animation]

        # TODO: connect to "fusebox" to allow disabling

    def update(self, dt, game):
        if game.stealth == True:
            return

        for bullet in self.bullets:
            bullet.update(dt, game)

        super().update(dt)

        if self.current_frame == 1 and not self.shot_frame and self.active:
            self.shoot()
            self.shot_frame = True
        
        if self.current_frame == 2:
            self.shot_frame = False

    def shoot(self):
        dir = (0, 0)

        match self.direction:
            case "UP":
                dir = (0, -1)
            case "RIGHT":
                dir = (1, 0)
            case "DOWN":
                dir = (0, 1)
            case "LEFT":
                dir = (-1, 0)

        self.bullets.append(Pellet(self, self.rect.center, dir))
    
    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
    
    def disable(self, time):
        super().disable(time)
    
    def draw(self, surface):
        img = self.current_animation[self.current_frame]

        super().draw(surface, img)

        for bullet in self.bullets:
            bullet.draw(surface)

class Pellet:

    def __init__(self, turret, pos, dir):
        self.turret = turret

        self.size = constants.VIRTUAL_TILE / 8

        self.speed = 60

        self.rect = pygame.Rect(pos[0] - self.size / 2, pos[1] - self.size / 2, self.size, self.size)
        self.dir = pygame.Vector2(dir[0], dir[1])

    def update(self, dt, game):
        center = pygame.Vector2(self.rect.center)
        center += self.dir * self.speed * dt

        self.rect.center = (round(center.x), round(center.y))

        if self.rect.colliderect(game.player.get_hitbox()):
            self.turret.remove_bullet(self)

            game.player.hit(10)
            game.trigger_alarm()

        if self.rect.bottom < 0 or self.rect.top > constants.VIRTUAL_HEIGHT or self.rect.right < 0 or self.rect.left > constants.VIRTUAL_WIDTH:
            self.turret.remove_bullet(self)

        for obj in game.level.get_solids():
            if self.rect.colliderect(obj.rect):
                self.turret.remove_bullet(self)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)