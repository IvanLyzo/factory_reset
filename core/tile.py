import pygame
from enum import Enum

class Tile:

    def __init__(self, rect, type):
        self.rect = rect
        self.type = type

        self.image = type.image

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class TileType(Enum):
    FLOOR = (0, False, "floor1.png")
    WALL = (1, True, "wall1.png")

    def __init__(self, code, collision, filename):
        self.code = code
        self.collision = collision

        self.filename = filename
        self.image = None
    
    @classmethod
    def load_images(cls):
        for member in cls:
            member.image = pygame.image.load(f"assets/tiles/{member.filename}").convert()