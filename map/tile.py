import pygame
from enum import Enum
import random

import constants

from core.gameobject import GameObject

# all possible tile types with their properties (code, collision, image file, base height)
class TileType(Enum):
    FLOOR = (0, False, "floor1", 1)
    PIT = (1, True, "pit/pit", 1, "pit/pit_top_floor", 3)
    WALL = (2, True, "wall/wall", 1, "wall/wall_bottom_floor", 1)

    def __init__(self, code: int, collision: bool, f_base: str, variations_base: int, f_alt: str = None, variations_alt: int = 0, collision_height: int = 16):
        self.code: int = code
        self.collision: bool = collision

        self.f_base: str = f_base
        self.variations_base: int = variations_base

        self.base: list[pygame.Surface] = []

        self.f_alt: str = f_alt
        self.variations_alt: int = variations_alt

        self.alt: list[pygame.Surface] = []

    # loads all tile images from disk
    @classmethod
    def load_images(cls):

        # for every tile type
        for member in cls:
            
            # load base
            if member.variations_base == 1:
                member.base.append(pygame.image.load(f"assets/tiles/{member.f_base}.png").convert())

            # load base variations
            else:
                for i in range(member.variations_base):
                    member.base.append(pygame.image.load(f"assets/tiles/{member.f_base}{i + 1}.png").convert())

            # load alt
            if member.variations_alt == 1:
                member.alt.append(pygame.image.load(f"assets/tiles/{member.f_alt}.png").convert())

            # load alt variations
            elif member.variations_alt > 1:
                for i in range(member.variations_alt):
                    member.alt.append(pygame.image.load(f"assets/tiles/{member.f_alt}{i + 1}.png").convert())

    # returns list of tile codes that are solid
    @classmethod
    def get_solids(cls):
        return [member.code for member in cls if member.collision]
    
    # returns tiletype by code
    @classmethod
    def get_by_code(cls, code: int):
        for member in cls:
            if member.code == code:
                return member
        raise ValueError(f"No TileType found for code {code}")

# represents direction of an object (includes movement vector and angle for rotation)
class Direction(Enum):
    UP = (pygame.math.Vector2(0, -1), 0)
    LEFT = (pygame.math.Vector2(-1, 0), 90)
    DOWN = (pygame.math.Vector2(0, 1), 180)
    RIGHT = (pygame.math.Vector2(1, 0), 270)

    def __init__(self, vector: pygame.math.Vector2, img_angle: int):
        self.vector: pygame.math.Vector2 = vector
        self.img_angle: int = img_angle

class Tile(GameObject):

    def __init__(self, pos: pygame.math.Vector2, grid: list[list[int]], type: TileType):
        pixel_pos = pygame.math.Vector2(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE)

        # Default base_height of 16, changed based on tile if not
        base_height = 16

        if type == TileType.WALL:
            base_height = 10

        # Determine adjacency and pick correct image variant
        self.type: TileType = type
        self.image = self.choose_image(pos, grid, type)

        # Pass collision and height info to parent
        super().__init__(pixel_pos, type.collision, base_height = base_height)

    def choose_image(self, pos: pygame.math.Vector2, grid: list[list[int]], type: TileType):
        x, y = int(pos.x), int(pos.y)

        # Get neighbors safely
        def get_tile_code(nx, ny):
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                return grid[ny][nx]
            return None

        above = get_tile_code(x, y - 1)
        below = get_tile_code(x, y + 1)

        # PIT: if above is floor, use alt variant
        if type == TileType.PIT and above != TileType.PIT.code and type.alt:
            return random.choice(type.alt)

        # WALL: if below is wall, use alt variant
        if type == TileType.WALL and below == TileType.WALL.code and type.alt:
            return random.choice(type.alt)

        # Default: random base variant
        return random.choice(type.base)

    # returns the rects used for collision (feet only)
    def feet(self):
        return [self.rect]

    # draws tile image to surface
    def draw(self, surface: pygame.Surface):
        super().draw(surface, self.image)