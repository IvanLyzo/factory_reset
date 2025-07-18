import pygame
from constants import *

class Enemy:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0] - VIRTUAL_TILE / 2, pos[1] - VIRTUAL_TILE / 2, VIRTUAL_TILE, VIRTUAL_TILE)
        self.active = True

        pass

    def update(self, dt, player):
        pass

    def draw(self, surface):
        pass