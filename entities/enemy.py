import pygame
from constants import *

class Enemy:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0] - VIRTUAL_TILE / 2, pos[1] - VIRTUAL_TILE / 2, VIRTUAL_TILE, VIRTUAL_TILE)
        self.active = True

        pass

    def update(self, dt, player):
        if self.active == False:
            self.disable_clock -= min(dt, self.disable_clock)

            if self.disable_clock == 0:
                self.active = True

        pass

    def disable(self, time):
        self.active = False
        self.disable_clock = time
    
    def draw(self, surface):
        pass