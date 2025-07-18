import pygame

from entities.enemy import Enemy

class OfficeDrone(Enemy):

    def __init__(self, pos, targets):
        super().__init__(pos)

        self.speed = 50
        self.targets = targets
        self.target_index = 0

        # load animations in the future

        pass

    def update(self, dt, player):
        super().update(dt, player)

        if self.active == False:
            return

        # move to current target
        target = self.targets[self.target_index]
        if target[0] > self.rect.center[0]:
            self.rect.x += min(self.speed * dt, target[0] - self.rect.center[0])
        elif target[0] < self.rect.center[0]:
            self.rect.x -= min(self.speed * dt, self.rect.center[0] - target[0])

        if target[1] > self.rect.center[1]:
            self.rect.y += min(self.speed * dt, target[1] - self.rect.center[1])
        elif target[1] < self.rect.center[1]:
            self.rect.y -= min(self.speed * dt, self.rect.center[1] - target[1])

        # switch targets if needed
        if self.rect.center == self.targets[self.target_index]:
            self.target_index = (self.target_index + 1) % len(self.targets)
        
        # check if "found" player
        if self.rect.colliderect(player.rect):
            player.found(self)

    def disable(self, time):
        super().disable(time)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

        pass