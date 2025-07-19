import pygame
from enum import Enum

from constants import *

class Tile:

    def __init__(self, pos, type):
        self.draw_rect = pygame.Rect(pos[0] * VIRTUAL_TILE, pos[1] * VIRTUAL_TILE, VIRTUAL_TILE, VIRTUAL_HEIGHT)

        self.rect = pygame.Rect(
            pos[0] * VIRTUAL_TILE,
            pos[1] * VIRTUAL_TILE + 6,  # +10 to place feet lower in tile
            VIRTUAL_TILE,
            10  # collision height only at the feet
        )
        self.type = type

        self.image = type.image

    def draw(self, surface):
        surface.blit(self.image, (self.draw_rect.x, self.draw_rect.y))

class TileType(Enum):
    FLOOR = (0, False, "floor1.png")
    WALL = (1, True, "wall1.png")
    ROOF = (2, True, "roof.png")

    def __init__(self, code, collision, filename):
        self.code = code
        self.collision = collision

        self.filename = filename
        self.image = None
    
    @classmethod
    def load_images(cls):
        for member in cls:
            member.image = pygame.image.load(f"assets/tiles/{member.filename}").convert()

    @classmethod
    def get_solids(cls):
        return [1, 2]