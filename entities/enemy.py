import pygame
from constants import *
from utils import *

class Enemy:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0] * VIRTUAL_TILE, pos[1] * VIRTUAL_TILE, VIRTUAL_TILE, VIRTUAL_TILE)
        self.active = True

        self.animations = {
            "idle": load_animation("player/idle"),
            "up": load_animation("player/walk_up"),
            "down": load_animation("player/walk_down"),
            "side": load_animation("player/walk_side")
        }
        self.current_animation = self.animations["idle"]

        self.current_frame = 0

        self.last_update = pygame.time.get_ticks()

        pass

    def update(self, dt):
        if self.active == False:
            self.disable_clock -= min(dt, self.disable_clock)

            if self.disable_clock == 0:
                self.active = True

        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = now

        pass

    def disable(self, time):
        self.active = False
        self.disable_clock = time
    
    def draw(self, surface):
        img = self.current_animation[self.current_frame]

        surface.blit(img, (self.rect.x, self.rect.y))