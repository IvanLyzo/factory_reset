import pygame

from constants import *
from entities.enemy import Enemy

class Turret(Enemy):

    def __init__(self, pos):
        super().__init__(pos)

        self.bullets = []

        self.shoot_interval = 2
        self.shoot_delay = 0

        # TODO: connect to "fusebox" to allow disabling

    def update(self, dt, player):
        super().update(dt, player)

        self.shoot_delay -= min(dt, self.shoot_delay)
        if self.shoot_delay == 0:
            self.shoot()
            self.shoot_delay = self.shoot_interval
        
        for bullet in self.bullets:
            bullet.update(dt)

    def shoot(self):
        # create new bullet
        self.bullets.append(Bullet(self.rect.center, (0, -1)))
    
    def disable(self, time):
        super().disable(time)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

        for bullet in self.bullets:
            bullet.draw(surface)

class Bullet:

    def __init__(self, pos, dir):
        self.size = VIRTUAL_TILE / 8

        self.speed = 60

        self.rect = pygame.Rect(pos[0] - self.size / 2, pos[1] - self.size / 2, self.size, self.size)
        self.dir = pygame.Vector2(dir[0], dir[1])

    def update(self, dt):
        center = pygame.Vector2(self.rect.center)
        center += self.dir * self.speed * dt

        self.rect.center = (round(center.x), round(center.y))

    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)