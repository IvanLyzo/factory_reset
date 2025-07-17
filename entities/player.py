import pygame
from constants import *

class Player:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0] - VIRTUAL_TILE / 2, pos[1] - VIRTUAL_TILE / 2, VIRTUAL_TILE, VIRTUAL_TILE)
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.speed = 100
        self.color = (255, 255, 0)
        
        self.facing = "down"

    def handle_input(self, event):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity.y = -1
            self.facing = "up"
        elif keys[pygame.K_s]:
            self.velocity.y = 1
            self.facing = "down"
        elif keys[pygame.K_a]:
            self.velocity.x = -1
            self.facing = "left"
        elif keys[pygame.K_d]:
            self.velocity.x = 1
            self.facing = "right"

    def move(self, map, dt):
        self.rect.x += self.velocity.x * self.speed * dt
        self.rect.y += self.velocity.y * self.speed * dt

        flat_map = [tile for row in map for tile in row]
        for tile in flat_map:
            if self.rect.colliderect(tile.rect) and tile.type.code == 1:

                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.rect.right

                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                elif self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom

        self.velocity.x = 0
        self.velocity.y = 0

    def draw(self, surface):
        # Placeholder: just color change for now
        colors = {
            "up": (255, 200, 200),
            "down": (255, 255, 0),
            "left": (200, 200, 255),
            "right": (200, 255, 200)
        }

        pygame.draw.rect(surface, colors[self.facing], self.rect)