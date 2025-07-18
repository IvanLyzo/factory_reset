import pygame

from constants import *

from entities.enemy import Enemy

class OfficeDrone(Enemy):

    def __init__(self, pos, targets):
        super().__init__(pos)

        self.speed = 50

        self.targets = []
        for target in targets:
            self.targets.append((target[0] * VIRTUAL_TILE, target[1] * VIRTUAL_TILE))

        self.target_index = 0

        self.animation_speed = 125

        pass

    def update(self, dt, player):
        super().update(dt)

        if self.active == False:
            return

        # move to current target
        target = self.targets[self.target_index]
        if target[0] > self.rect.x:
            self.rect.x += min(self.speed * dt, target[0] - self.rect.x)
        elif target[0] < self.rect.x:
            self.rect.x -= min(self.speed * dt, self.rect.x - target[0])

        if target[1] > self.rect.y:
            self.rect.y += min(self.speed * dt, target[1] - self.rect.y)
        elif target[1] < self.rect.y:
            self.rect.y -= min(self.speed * dt, self.rect.y - target[1])

        # switch targets if needed
        if self.rect.topleft == self.targets[self.target_index]:
            self.target_index = (self.target_index + 1) % len(self.targets)
        
        # check if "found" player
        if self.rect.colliderect(player.rect):
            player.found(self)

    def disable(self, time):
        super().disable(time)
    
    def draw(self, surface):
        super().draw(surface)
        # pygame.draw.rect(surface, (255, 255, 255), self.rect)