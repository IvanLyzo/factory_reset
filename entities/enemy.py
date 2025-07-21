import pygame

import constants
import utils

class Enemy:

    def __init__(self, pos: pygame.math.Vector2):
        self.rect: pygame.Rect = pygame.Rect(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        self.active: bool = True

        self.animations: dict[str, list[pygame.Surface]] = {}
        self.animation_speed: int = 125

        self.current_frame: int = 0
        self.last_update: int = pygame.time.get_ticks()

        self.disable_clock: float = 0

    def update(self, dt: float):
        if self.active == False:
            self.disable_clock -= min(dt, self.disable_clock)

            if self.disable_clock == 0:
                self.active = True
            
            return

        now: int = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = now

    def disable(self, time: float):
        self.active = False
        self.disable_clock = time
    
    def draw(self, surface: pygame.Surface, img: pygame.Surface):
        surface.blit(img, self.rect.topleft)