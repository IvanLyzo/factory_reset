import json

from map.tile import Tile, TileType

from constants import *

class Level:

    def __init__(self, floor):
        
        with open("assets/levels/level_" + str(floor) + ".json", 'r') as data:
            self.level = json.load(data)

            self.load_room(0)

    def load_room(self, index):
        room = self.level["rooms"][index]

        self.enemies = room["enemies"]
        self.doors = room["doors"]

        self.grid = room["grid"]
            
        self.tilemap = []
        for y, row in enumerate(self.grid):
            self.tilemap.append([])
            for x, type in enumerate(row):
                match type:
                    case 0:
                        self.tilemap[y].append(Tile((x, y), TileType.FLOOR))
                    case 1:
                        self.tilemap[y].append(Tile((x, y), TileType.WALL))
                    case 2:
                        self.tilemap[y].append(Tile((x, y), TileType.ROOF))
    
    def get_walls(self):
        tiles = [tile for row in self.tilemap for tile in row]

        objs = []
        for tile in tiles:
            if tile.type.code in TileType.get_solids():
                objs.append(tile)
        
        return objs
    
    def draw_floor(self, screen):
        for y, row in enumerate(self.tilemap):
            for x, tile in enumerate(row):
                if tile.type.code == 0:
                    tile.draw(screen)