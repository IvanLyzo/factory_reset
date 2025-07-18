import json
import pygame

from core.tile import Tile, TileType

from constants import *

class Level:

    def __init__(self, floor):
        
        with open("assets/levels/level_" + str(floor) + ".json", 'r') as data:
            level = json.load(data)

            self.player_spawn = level["player_spawn"]
            self.enemies = level["enemies"]

            self.grid = level["tiles"]
            self.room = []
            for y, row in enumerate(self.grid):
                self.room.append([])
                for x, type in enumerate(row):
                    if type == 0:
                        self.room[y].append(Tile((x, y), TileType.FLOOR))
                    elif type == 1:
                        self.room[y].append(Tile((x, y), TileType.WALL))

    
    def get_walls(self):
        tiles = [tile for row in self.room for tile in row]

        objs = []
        for tile in tiles:
            if tile.type.code != 0:
                objs.append(tile)
        
        return objs
    
    def draw_floor(self, screen):
        for y, row in enumerate(self.room):
            for x, tile in enumerate(row):
                if tile.type.code == 0:
                    tile.draw(screen)