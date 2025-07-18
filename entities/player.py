import pygame
from constants import *
from utils import *

class Player:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0] - VIRTUAL_TILE / 2, pos[1] - VIRTUAL_TILE / 2, VIRTUAL_TILE, VIRTUAL_TILE)
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.speed = 50

        self.animations = {
            "idle": load_animation("player/idle"),
            "up": load_animation("player/walk_up"),
            "down": load_animation("player/walk_down"),
            "side": load_animation("player/walk_side")
        }
        self.current_animation = self.animations["idle"]
        self.flip = False

        self.current_frame = 0
        self.animation_speed = 150

        self.last_update = pygame.time.get_ticks()
    
    def handle_input(self, keys):
        if keys[pygame.K_w]:
            self.velocity.y = -1
            self.current_animation = self.animations["up"]

        elif keys[pygame.K_s]:
            self.velocity.y = 1
            self.current_animation = self.animations["down"]

        elif keys[pygame.K_a]:
            self.velocity.x = -1
            self.current_animation = self.animations["side"]
            self.flip = True

        elif keys[pygame.K_d]:
            self.velocity.x = 1
            self.current_animation = self.animations["side"]
            self.flip = False

    def move(self, map, dt):
        if self.velocity == pygame.math.Vector2(0, 0):
            self.current_animation = self.animations["idle"]

        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = now

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

    def emp(self, enemies):
        print("emp active")

        player_pos = pygame.math.Vector2(self.rect.center)

        for enemy in enemies:
            enemy_pos = pygame.math.Vector2(enemy.rect.center)
            distance = player_pos.distance_to(enemy_pos)

            if distance < 100:
                print("disable")
                enemy.disable(3)
    
    def found(self, enemy):
        print("Found me!")

    def draw(self, surface):
        img = self.current_animation[self.current_frame]
        if self.flip == True:
            img = pygame.transform.flip(img, True, False)

        surface.blit(img, (self.rect.x, self.rect.y))