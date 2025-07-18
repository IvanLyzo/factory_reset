import pygame

from constants import *
from entities.enemy import Enemy

class Turret(Enemy):

    def __init__(self, pos):
        super().__init__(pos)

        self.bullets = []

        self.shoot_interval = 2
        self.shoot_delay = 0

        self.animation_speed = 500

        # TODO: connect to "fusebox" to allow disabling

    def update(self, dt, player):
        super().update(dt)

        self.shoot_delay -= min(dt, self.shoot_delay)
        if self.shoot_delay == 0:
            self.shoot()
            self.shoot_delay = self.shoot_interval
        
        for bullet in self.bullets:
            bullet.update(dt, player)

    def shoot(self):
        # create new bullet
        self.bullets.append(Pellet(self, self.rect.center, (0, -1)))
    
    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
    
    def disable(self, time):
        super().disable(time)
    
    def draw(self, surface):
        super().draw(surface)
        # pygame.draw.rect(surface, (255, 255, 255), self.rect)

        for bullet in self.bullets:
            bullet.draw(surface)

class Pellet:

    def __init__(self, turret, pos, dir):
        self.turret = turret

        self.size = VIRTUAL_TILE / 8

        self.speed = 60

        self.rect = pygame.Rect(pos[0] - self.size / 2, pos[1] - self.size / 2, self.size, self.size)
        self.dir = pygame.Vector2(dir[0], dir[1])

    def update(self, dt, player):
        center = pygame.Vector2(self.rect.center)
        center += self.dir * self.speed * dt

        self.rect.center = (round(center.x), round(center.y))

        if self.rect.bottom < 0 or self.rect.top > VIRTUAL_HEIGHT or self.rect.right < 0 or self.rect.left > VIRTUAL_WIDTH:
            self.turret.remove_bullet(self)
        
        if self.rect.colliderect(player.rect):
            self.turret.remove_bullet(self)
            player.hit(self)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)