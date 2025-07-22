# type: ignore

import json
import pygame

import constants
import utils

from entities.enemy import Enemy

from map.tile import Tile, TileType, Direction
from map.trigger import Trigger

from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret
from entities.enemies.laser import Laser

class Floor:

    def __init__(self, game: "GameWindow", floor: int,):
        self.level = utils.load_json("levels/level_" + str(floor))

        self.player_spawn: pygame.math.Vector2 = pygame.math.Vector2(self.level["player_spawn"][0], self.level["player_spawn"][1])
        self.load_room(game, 0)

    def load_room(self, game: "GameWindow", room_index: int):
        room: list[list[int]] = self.level["rooms"][room_index]

        self.gen_tilemap(room.get("grid"))

        self.gen_elevator(room.get("elevator"), game)
        self.gen_doors(room.get("doors"), game)

        self.gen_enemies(room.get("enemies"))
    
    def gen_tilemap(self, grid: list[list[int]]):
        self.tilemap: list[list[Tile]] = []

        for y, row in enumerate(grid):
            self.tilemap.append([])
            for x, type in enumerate(row):
                pos = pygame.math.Vector2(x, y)

                match type:
                    case 0:
                        self.tilemap[y].append(Tile(pos, TileType.FLOOR))
                    case 1:
                        self.tilemap[y].append(Tile(pos, TileType.WALL))
                    case 2:
                        self.tilemap[y].append(Tile(pos, TileType.ROOF))
    
    def gen_elevator(self, elevator_data, game: "GameWindow"):
        if elevator_data != None:
            self.elevator: Trigger = Trigger(utils.get_bounds(elevator_data["tiles"]), lambda: game.generate_floor(elevator_data["to_floor"]))
            self.elevator_room: bool = True
        else:
            self.elevator_room: bool = False
    
    def gen_doors(self, door_data, game: "GameWindow"):
        self.doors: dict[int, Trigger] = {}

        for door in door_data:
            rect: pygame.Rect = utils.get_bounds(door["tiles"])
            
            id: int = door["id"]
            to_room: int = door["to_room"]

            self.doors[id] = Trigger(rect, lambda: game.switch_room(to_room, id))
    
    def gen_enemies(self, enemy_data):
        self.enemies: list[Enemy] = []

        for enemy in enemy_data:
            type: str = enemy["type"]
            spawn: pygame.math.Vector2 = pygame.math.Vector2(enemy["spawn"][0], enemy["spawn"][1])

            if type == "DRONE":
                targets: list[pygame.math.Vector2] = []

                for target in enemy["targets"]:
                    targets.append(pygame.math.Vector2(target[0], target[1]))

                self.enemies.append(OfficeDrone(spawn, targets))
            
            elif type == "TURRET":
                direction: str = enemy["direction"]
                self.enemies.append(Turret(spawn, Direction[direction.upper()]))

            elif type == "LASER":
                catcher: pygame.math.Vector2 = pygame.math.Vector2(enemy["catcher"][0], enemy["catcher"][1])
                fusebox: pygame.math.Vector2 = pygame.math.Vector2(enemy["fusebox"][0], enemy["fusebox"][1])
                direction: str = enemy["direction"]

                self.enemies.append(Laser(spawn, catcher, fusebox, Direction[direction.upper()]))
    
    def get_solids(self):
        tiles: list[Tile] = [tiles for row in self.tilemap for tiles in row]

        solids: list[Tile] = []
        for tile in tiles:
            if tile.type.code in TileType.get_solids():
                solids.append(tile)
        
        return solids
    
    def draw_floor(self, screen: pygame.Surface):
        for y, row in enumerate(self.tilemap):
            for x, tile in enumerate(row):
                if tile.type.code == 0:
                    tile.draw(screen)