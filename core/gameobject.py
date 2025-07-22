import pygame
import constants

# base GameObject class for all in-game objects (tiles, enemies, player)
class GameObject:

    def __init__(self, pos: pygame.math.Vector2, solid: bool, base_height:int = 8):

        # store position in vector2 for subpixel float precision
        self.pos: pygame.math.Vector2 = pos
        
        # if solid (has collison) store collision rect in rect (integers only)
        self.solid: bool = solid
        if solid:
            self.collision_rect: pygame.Rect = pygame.Rect(pos.x, pos.y + constants.VIRTUAL_TILE - base_height, constants.VIRTUAL_TILE, base_height)
        
        # active flag for GameObject
        self.active: bool = True

        # animation fields
        self.animations: dict[str, list[pygame.Surface]] = {} # dictionary of animations
        self.animation_speed: int = 125 # speed (in ms) between frames

        self.current_frame: int = 0 # current frame index
        self.last_update: int = pygame.time.get_ticks() # last time updated

    # move GameObject to a certain position in px
    def move_to(self, pos: pygame.math.Vector2):
        
        # update position
        self.pos = pos

        # if solid, update collision (will update every several frames because of int truncation)
        if self.solid:
            self.collision_rect = pygame.Rect(pos.x, pos.y + 10, constants.VIRTUAL_TILE, 6)
    
    # update GameObject (regardless of active or not, subclasses decide that)
    def update(self):

        # current time since start (in ms)
        now: int = pygame.time.get_ticks()

        # if delta time between updates passed animation speed
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation) # rotate animation
            self.last_update = now # save current time

    # draw GameObject
    def draw(self, surface: pygame.Surface, img: pygame.Surface):
        surface.blit(img, self.pos) # draw image on surface at position
