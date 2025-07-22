import pygame
from enum import Enum

import constants

from core.gameobject import GameObject

class TileType(Enum):
    FLOOR = (0, False, "floor1.png")
    WALL = (1, True, "wall1.png", 10)
    ROOF = (2, True, "roof.png", 16)

    def __init__(self, code: int, collision: bool, filename: str, base_height: int = 0):
        self.code: int = code
        self.collision: bool = collision

        if collision:
            self.base_height = base_height

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

class Tile(GameObject):

    def __init__(self, pos: pygame.math.Vector2, type: TileType):
        if type.collision:
            super().__init__(pygame.math.Vector2(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE), True, base_height = type.base_height)
        else:
            super().__init__(pygame.math.Vector2(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE), False)

        self.type: TileType = type
        self.image: pygame.Surface = type.image

    def feet(self):
        return [self.rect]
    
    def draw(self, surface: pygame.Surface):
        super().draw(surface, self.image)