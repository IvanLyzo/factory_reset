import json
import pygame

from core.tile import Tile, TileType

from constants import *

class Level:

    def __init__(self, floor):
        
        with open("assets/levels/level_" + str(floor) + ".json", 'r') as data:
            level = json.load(data)

            self.grid = level["tiles"]

            self.room = []
            
            for y, row in enumerate(self.grid):
                self.room.append([])
                for x, type in enumerate(row):

                    if type == 0:
                        self.room[y].append(Tile(pygame.Rect(x * VIRTUAL_TILE, y * VIRTUAL_TILE, VIRTUAL_TILE, VIRTUAL_TILE), TileType.FLOOR))
                    elif type == 1:
                        self.room[y].append(Tile(pygame.Rect(x * VIRTUAL_TILE, y * VIRTUAL_TILE, VIRTUAL_TILE, VIRTUAL_TILE), TileType.WALL))

    
    def draw(self, screen):
        for y, row in enumerate(self.room):
            for x, tile in enumerate(row):
                tile.draw(screen)