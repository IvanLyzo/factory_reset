import pygame
from enum import Enum

import constants
from core.gameobject import GameObject

# all possible tile types with their properties (code, collision, image file, base height)
class TileType(Enum):
    FLOOR = (0, False, "floor1.png")
    WALL = (1, True, "wall1.png", 10)
    ROOF = (2, True, "roof.png", 16)

    def __init__(self, code: int, collision: bool, filename: str, base_height: int = 0):
        self.code: int = code
        self.collision: bool = collision

        # only store height if tile is solid (for depth sorting)
        if collision:
            self.base_height = base_height

        self.filename: str = filename
        self.image: pygame.Surface | None = None

    # loads all tile images from disk
    @classmethod
    def load_images(cls):
        for member in cls:
            member.image = pygame.image.load(f"assets/tiles/{member.filename}").convert()

    # returns list of tile codes that are solid
    @classmethod
    def get_solids(cls):
        return [1, 2]

# represents direction of an object (includes movement vector and angle for rotation)
class Direction(Enum):
    UP = (pygame.math.Vector2(0, -1), 0)
    LEFT = (pygame.math.Vector2(-1, 0), 90)
    DOWN = (pygame.math.Vector2(0, 1), 180)
    RIGHT = (pygame.math.Vector2(1, 0), 270)

    def __init__(self, vector: pygame.math.Vector2, img_angle: int):
        self.vector: pygame.math.Vector2 = vector
        self.img_angle: int = img_angle

# tile object used in tilemap (extends GameObject for positioning and collision)
class Tile(GameObject):

    def __init__(self, pos: pygame.math.Vector2, type: TileType):
        pixel_pos = pygame.math.Vector2(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE)

        # pass collision and height info to parent GameObject
        if type.collision:
            super().__init__(pixel_pos, True, base_height=type.base_height)
        else:
            super().__init__(pixel_pos, False)

        self.type: TileType = type
        self.image: pygame.Surface = type.image

    # returns the rects used for collision (feet only)
    def feet(self):
        return [self.rect]

    # draws tile image to surface
    def draw(self, surface: pygame.Surface):
        super().draw(surface, self.image)