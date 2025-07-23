# imports used to delay certain module imports to avoid circular import
from __future__ import annotations
from typing import TYPE_CHECKING

# delayed imports
if TYPE_CHECKING:
    from entities.enemies.laser import Laser
    from windows.gamewindow import GameWindow

# normal imports
import pygame

import constants
import utils

from core.gameobject import GameObject
from windows.hackwindow import HackWindow, HackState

# Laser's Fusebox class (inherits GameObject)
class Fusebox(GameObject):

    def __init__(self, pos: pygame.math.Vector2, laser: Laser):
        super().__init__(pygame.math.Vector2(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE), True, 6)
        self.laser: Laser = laser

        # setup animation fields for fusebox (inherited from superclass GameObject)
        self.animations["active"] = utils.load_animation("enemies/laser/fusebox/active")
        self.animations["disabled"] = utils.load_animation("enemies/laser/fusebox/disabled", 1)
        self.current_animation: list[pygame.Surface] = [pygame.transform.rotate(frame, self.laser.direction.img_angle) for frame in self.animations["active"]]

        # hack window
        self.window: HackWindow = HackWindow()

    # interact with fusebox
    def interact(self, game: GameWindow):

        # get player center as vector2
        player_pos: pygame.math.Vector2 = pygame.math.Vector2(game.player.collision_rect.centerx, game.player.collision_rect.centery)

        # get vector distance between fusebox and player
        distance: float = player_pos.distance_to(self.collision_rect.center)
        
        # if within interactable range and still in stealth mode
        if distance < constants.INTERACT_RANGE and game.stealth == True:
            game.start_minigame(self.window) # tell game to start our window as minigame
            self.window.active = True # activate window
    
    def update(self):
        super().update()

        if self.window.state == HackState.PASSED:
            self.current_animation = [pygame.transform.rotate(frame, self.laser.direction.img_angle) for frame in self.animations["disabled"]]
            self.current_frame = 0

            self.laser.active = False

    # draw fusebox
    def draw(self, surface: pygame.Surface):
        img = self.current_animation[self.current_frame]
        super().draw(surface, img)