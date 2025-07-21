import pygame
import constants
import utils

class Player:

    def __init__(self, pos):
        self.alive = True

        self.rect = pygame.Rect(pos[0] * constants.VIRTUAL_TILE, pos[1] * constants.VIRTUAL_TILE + 8, constants.VIRTUAL_TILE, 8)

        self.health_cap = 100 # TODO: remove temp health cap used for testing
        self.current_health = self.health_cap

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 50

        self.animations = {
            "idle": utils.load_animation("player/idle"),
            "up": utils.load_animation("player/walk_up"),
            "down": utils.load_animation("player/walk_down"),
            "side": utils.load_animation("player/walk_side")
        }
        self.current_animation = self.animations["idle"]
        self.flip = False
        self.current_frame = 0
        self.animation_speed = 125
        self.last_update = pygame.time.get_ticks()
    
    def set_pos(self, pos: pygame.math.Vector2):
        self.rect = pygame.Rect(pos.x * constants.VIRTUAL_TILE, pos.y * constants.VIRTUAL_TILE + 8, constants.VIRTUAL_TILE, 8)
    
    def get_hitbox(self):
        return pygame.Rect(self.rect.left, self.rect.top - 8, self.rect.width, self.rect.height + 8)
    
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

    def update(self, game, dt):
        if self.velocity == pygame.math.Vector2(0, 0):
            self.current_animation = self.animations["idle"]

        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = now

        self.rect.x += self.velocity.x * self.speed * dt
        self.rect.y += self.velocity.y * self.speed * dt

        for obj in game.solids:
            if obj == self:
                continue

            if self.rect.colliderect(obj.rect):

                if self.velocity.x > 0:
                    self.rect.right = obj.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = obj.rect.right

                if self.velocity.y > 0:
                    self.rect.bottom = obj.rect.top
                elif self.velocity.y < 0:
                    self.rect.top = obj.rect.bottom

        self.velocity.x = 0
        self.velocity.y = 0

    def emp(self, enemies):
        player_pos = pygame.math.Vector2(self.rect.center)

        for enemy in enemies:
            enemy_pos = pygame.math.Vector2(enemy.rect.center)
            distance = player_pos.distance_to(enemy_pos)

            if distance < 100:
                print("disable")
                enemy.disable(3)

    def hit(self, dmg):
        self.current_health -= min(dmg, self.current_health)

        if self.current_health == 0:
            print("die once") # TODO: reset level on death (+ possibly other things)
            self.health_cap -= min(25, self.health_cap)
            print("lowered health to ", self.health_cap)
            if self.health_cap == 0:
                self.alive = False
            self.current_health = self.health_cap

    def draw(self, surface):
        img = self.current_animation[self.current_frame]

        if self.flip:
            img = pygame.transform.flip(img, True, False)

        draw_x = self.rect.centerx - img.get_width() // 2
        draw_y = self.rect.bottom - img.get_height()

        surface.blit(img, (draw_x, draw_y))
