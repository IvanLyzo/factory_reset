import pygame
import constants

from core.gameobject import GameObject

# base Enemy class that inherits GameObject and acts as superclass for all enemy types
class Enemy(GameObject):

    def __init__(self, pos: pygame.math.Vector2, solid: bool, base_height: int = 8):

        # call super init (after converting tilemap pos to pixel pos - all enemies will pass in tilemap pos from JSON data)
        super().__init__(pygame.math.Vector2(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE), solid, base_height)

        # time until enabled again
        self.disable_clock: float = 0

    # update enemies
    def update(self, dt: float):

        # if not active
        if self.active == False:

            # count down until 0 (active)
            self.disable_clock -= min(dt, self.disable_clock)

            # enable once clock reached 0
            if self.disable_clock == 0:
                self.active = True
            
            return

        # update superclass if active
        super().update()