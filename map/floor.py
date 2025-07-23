# imports used to delay certain module imports to avoid circular import
from __future__ import annotations
from typing import TYPE_CHECKING

# delayed imports
if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

# normal imports
import pygame

import utils

from typing import Any

from entities.enemy import Enemy
from entities.enemies.officedrone import OfficeDrone
from entities.enemies.turret import Turret
from entities.enemies.laser import Laser

from map.tile import Tile, TileType, Direction
from map.trigger import Trigger

# level floor class manages tilemap, triggers, and enemies for a given floor
class Floor:

    def __init__(self, game: GameWindow, floor: int):
        
        # load JSON level data and spawn point
        self.level: dict[str, Any] = utils.load_json("levels/level_" + str(floor))
        self.player_spawn: pygame.math.Vector2 = pygame.math.Vector2(self.level["player_spawn"][0], self.level["player_spawn"][1])

        # load first room (room 0) immediately
        self.load_room(game, 0)

    # parses and generates all data needed to load a room: tiles, triggers, and enemies
    def load_room(self, game: GameWindow, room_index: int):
        room: dict[str, Any] = self.level["rooms"][room_index]

        self.gen_tilemap(room.get("grid"))
        self.gen_elevator(room.get("elevator"), game)
        self.gen_doors(room.get("doors"), game)
        self.gen_enemies(room.get("enemies"))

    # creates the tilemap grid from a 2D array of integer codes
    def gen_tilemap(self, grid: list[list[int]]):

        self.tilemap: list[list[Tile]] = [] # tilemap
        
        for y, row in enumerate(grid):
            self.tilemap.append([]) # append row

            for x, type in enumerate(row):
                pos = pygame.math.Vector2(x, y) # vector position
                
                # generate tile based on code
                match type:
                    case 0:
                        self.tilemap[y].append(Tile(pos, TileType.FLOOR))
                    case 1:
                        self.tilemap[y].append(Tile(pos, TileType.WALL))
                    case 2:
                        self.tilemap[y].append(Tile(pos, TileType.ROOF))

    # creates the elevator trigger if the room has one
    def gen_elevator(self, elevator_data: dict[str, Any] | None, game: GameWindow):
        
        # create elevator trigger if elevator exists and flag room
        if elevator_data is not None:
            self.elevator: Trigger = Trigger(utils.get_bounds(elevator_data["tiles"]), lambda: game.gen_floor(elevator_data["to_floor"]))
            self.elevator_room: bool = True
        
        # flag room as not having an elevator
        else:
            self.elevator_room: bool = False

    # generates door triggers and maps them by ID
    def gen_doors(self, door_data: list[dict[str, Any]], game: GameWindow):

        self.doors: dict[int, Trigger] = {}
        
        # loop through all doors in room
        for door in door_data:
            
            # get all door values
            rect: pygame.Rect = utils.get_bounds(door["tiles"])
            id: int = door["id"]
            to_room: int = door["to_room"]

            self.doors[id] = Trigger(rect, lambda: game.switch_room(to_room, id)) # create door

    # creates enemies in room based on JSON
    def gen_enemies(self, enemy_data: list[dict[str, Any]]):

        self.enemies: list[Enemy] = []

        # loop through all enemies in room
        for enemy in enemy_data:

            # get generic enemy data
            type: str = enemy["type"]
            spawn: pygame.math.Vector2 = pygame.math.Vector2(enemy["spawn"][0], enemy["spawn"][1])

            # create drone
            if type == "DRONE":
                
                # get targets for drone
                targets: list[pygame.math.Vector2] = []
                for target in enemy["targets"]:
                    targets.append(pygame.math.Vector2(target[0], target[1]))
                
                # append drone
                self.enemies.append(OfficeDrone(spawn, targets))

            # create turret
            elif type == "TURRET":

                # get turret direction
                direction: str = enemy["direction"]

                # append turret
                self.enemies.append(Turret(spawn, Direction[direction.upper()]))

            # create laser
            elif type == "LASER":

                # get laser-specific info
                catcher: pygame.math.Vector2 = pygame.math.Vector2(enemy["catcher"][0], enemy["catcher"][1])
                fusebox: pygame.math.Vector2 = pygame.math.Vector2(enemy["fusebox"][0], enemy["fusebox"][1])
                direction: str = enemy["direction"]
                
                # append laser
                self.enemies.append(Laser(spawn, catcher, fusebox, Direction[direction.upper()]))

    # returns all tiles marked as solid for collisions
    def get_solids(self):

        # flat map of tiles
        tiles: list[Tile] = [tiles for row in self.tilemap for tiles in row]
        
        # populate list of solids based on code
        solids: list[Tile] = []
        for tile in tiles:
            if tile.type.code in TileType.get_solids():
                solids.append(tile)
        
        # return list of solids
        return solids

    # draws only floor tiles
    def draw_floor(self, screen: pygame.Surface):

        # loop through tilemap
        for x, row in enumerate(self.tilemap):
            for y, tile in enumerate(row):
                
                # draw tile if code is 0 (floor)
                if tile.type.code == 0:
                    tile.draw(screen)