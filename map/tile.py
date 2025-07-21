import pygame
from enum import Enum

from constants import *

class TileType(Enum):
    FLOOR = (0, False, "floor1.png")
    WALL = (1, True, "wall1.png")
    ROOF = (2, True, "roof.png")

    def __init__(self, code: int, collision: bool, filename: str):
        self.code: int = code
        self.collision: bool = collision

        self.filename: str = filename
        self.image: pygame.Surface | None = None
    
    @classmethod
    def load_images(cls):
        for member in cls:
            member.image = pygame.image.load(f"assets/tiles/{member.filename}").convert()

    @classmethod
    def get_solids(cls):
        return [1, 2]

class Direction(Enum):

    UP = (pygame.math.Vector2(0, -1), 0)
    LEFT = (pygame.math.Vector2(-1, 0), 90)
    DOWN = (pygame.math.Vector2(0, 1), 180)
    RIGHT = (pygame.math.Vector2(1, 0), 270)

    def __init__(self, vector: pygame.math.Vector2, img_angle: int):
        self.vector: pygame.math.Vector2 = vector
        self.img_angle: int = img_angle

class Tile:

    def __init__(self, pos: pygame.math.Vector2, type: TileType):
        self.draw_rect: pygame.Rect = pygame.Rect(pos.x * VIRTUAL_TILE, pos.y * VIRTUAL_TILE, VIRTUAL_TILE, VIRTUAL_HEIGHT)

        self.rect: pygame.Rect = pygame.Rect(pos.x * VIRTUAL_TILE, pos.y * VIRTUAL_TILE + 6, VIRTUAL_TILE, 10)
        self.type: TileType = type

        self.image: pygame.Surface = type.image

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.draw_rect.x, self.draw_rect.y))