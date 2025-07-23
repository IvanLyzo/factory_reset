# imports used to delay certain module imports to avoid circular import
from __future__ import annotations
from typing import TYPE_CHECKING

# delayed imports
if TYPE_CHECKING:
    from windows.gamewindow import GameWindow

# normal imports
import pygame

import constants
import utils

from core.gameobject import GameObject
from entities.enemy import Enemy

from ui.menuwindow import MenuWindow

# user-controlled player class inherits GameObject
class Player(GameObject):

    def __init__(self, pos: pygame.math.Vector2):
        super().__init__(pos, True)

        # boolean if died
        self.died: bool = False

        self.health_cap: int = 100 # current player health cap
        self.current_health: int = self.health_cap # current player health

        self.velocity: pygame.math.Vector2 = pygame.math.Vector2() # frame velocity
        self.speed: int = 50 # speed (px/sec)

        # setup animation fields for player (inherited from superclass GameObject)
        self.animations = {
            "idle": utils.load_animation("player/idle"),
            "up": utils.load_animation("player/walk_up"),
            "down": utils.load_animation("player/walk_down"),
            "side": utils.load_animation("player/walk_side")
        }
        self.current_animation: list[pygame.Surface] = self.animations["idle"]
        
        # player variable for left/right movement
        self.flip: bool = False

        # init player ui
        self.player_ui: MenuWindow = MenuWindow(0, custom_pos=pygame.Rect(constants.VIRTUAL_WIDTH - 120, constants.VIRTUAL_HEIGHT - 80, 100, 60))
        self.player_ui.add_element(20, "Cap: 100%", constants.p)
        self.player_ui.add_element(40, "Curr: 100%", constants.p)
        self.player_ui.active = True

        # countdown before hiding ui
        self.player_ui_countdown: float = 3
    
    # handle all player-related key input
    def handle_input(self, keys: list[int]):

        # moving up
        if keys[pygame.K_w]:
            self.velocity.y = -1
            self.current_animation = self.animations["up"]

        # moving down
        elif keys[pygame.K_s]:
            self.velocity.y = 1
            self.current_animation = self.animations["down"]

        # moving left
        elif keys[pygame.K_a]:
            self.velocity.x = -1
            self.current_animation = self.animations["side"]
            self.flip = True # side sprite is right-facing, so set flip to true

        # moving right
        elif keys[pygame.K_d]:
            self.velocity.x = 1
            self.current_animation = self.animations["side"]
            self.flip = False # side sprite is left-facing, no flip needed

    # update player
    def update(self, game: GameWindow, dt: float):
        self.player_ui_countdown -= min(dt, self.player_ui_countdown)
        if self.player_ui_countdown == 0:
            self.player_ui.active = False

        # set idle animation if no movement this frame
        if self.velocity == pygame.math.Vector2():
            self.current_animation = self.animations["idle"]

        # superclass update
        super().update()

        # perform movement
        if self.velocity != pygame.math.Vector2():
            self.move_to(self.pos + self.velocity * self.speed * dt)

        # check for collisions
        for obj in game.solids:

            # skip if player (don't want player checking collision with itself)
            if isinstance(obj, Player):
                continue

            # collision rect of current iterated game object
            rect = obj.collision_rect

            if self.collision_rect.colliderect(rect):
                new_pos = self.pos.copy()

                # Correct horizontal movement
                if self.velocity.x > 0:
                    new_pos.x = rect.left - self.collision_rect.width
                elif self.velocity.x < 0:
                    new_pos.x = rect.right

                # Correct vertical movement
                if self.velocity.y > 0:
                    new_pos.y = rect.top - constants.VIRTUAL_TILE
                elif self.velocity.y < 0:
                    new_pos.y = rect.bottom - (constants.VIRTUAL_TILE - self.collision_rect.height)

                self.move_to(new_pos)

        # reset velocity for next frame
        self.velocity = pygame.math.Vector2()

    # player emp ability (called by GameWindow)
    def emp(self, enemies: list[Enemy]):
        
        # loop through enemies
        for enemy in enemies:
            distance: float = self.pos.distance_to(enemy.pos) # distance from player to enemy

            # if in range, disable enemy for some time
            if distance < constants.EMP_RANGE:
                enemy.disable(constants.EMP_TIME)

    # hit function called to indicate damage player took
    def hit(self, dmg: int):
        
        # apply damage
        self.current_health -= min(dmg, self.current_health)

        # if died once
        if self.current_health == 0:
            self.died = True # set flag
            self.health_cap -= min(25, self.health_cap) # lower player cap

            # if perma-death
            if self.health_cap == 0:
                self.active = False # disable player
            
            # update current health to cap
            self.current_health = self.health_cap

        # update player ui
        self.player_ui.text[0].text = "Cap: " + str(self.health_cap) + "%"
        self.player_ui.text[1].text = "Curr: " + str(self.current_health) + "%"

        # show ui for another 3 seconds (then disappear to not cover screen)
        self.player_ui.active = True
        self.player_ui_countdown = 3

    # draw player
    def draw(self, surface: pygame.Surface):

        # get correct frame of current animation
        img: pygame.Surface = self.current_animation[self.current_frame]

        # flip if needed
        if self.flip:
            img = pygame.transform.flip(img, True, False)

        # draw player from superclass
        super().draw(surface, img)
