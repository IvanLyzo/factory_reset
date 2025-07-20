import pygame

import constants
import utils

class Enemy:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0] * constants.VIRTUAL_TILE, pos[1] * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE)
        self.active = True

        self.animations = {}

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self, dt):
        if self.active == False:
            self.disable_clock -= min(dt, self.disable_clock)

            if self.disable_clock == 0:
                self.active = True
            
            return

        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = now

    def disable(self, time):
        self.active = False
        self.disable_clock = time
    
    def draw(self, surface, img):
        surface.blit(img, (self.rect.x, self.rect.y))