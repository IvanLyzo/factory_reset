import sys
import pygame

import constants

from core.game import Game
from map.tile import TileType

# --------------------------
# ENTIRE PROGRAM ENTRY POINT
# --------------------------

# init pygame
pygame.init()

# create virtual game canvas
canvas: pygame.Surface = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT))

# create view screen (upscaled virtual canvas)
screen: pygame.Surface = pygame.display.set_mode((constants.screen_width, constants.screen_height))

# set title
pygame.display.set_caption("Factory Reset")

# set game clock
clock: pygame.time.Clock = pygame.time.Clock()

# load tile images into enum
TileType.load_images()

# load fonts
constants.h1 = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)
constants.p = pygame.font.Font("assets/PressStart2P-Regular.ttf", 8)

# create game
game: Game = Game()

# quit game function
def quit_game():
    pygame.quit()
    sys.exit()

# main game loop
running: bool = True
while running:

    # process all events this frame
    for event in pygame.event.get():

        # exit loop if user presses X in top right
        if event.type == pygame.QUIT:
            running = False
        
        # pass on all other events to game
        game.handle_event(event)
    
    # check if game requested quit (quit should only be done in here, not anywhere else in the game)
    if game.request_quit:
        quit_game()
    
    # update delta time for frame
    dt: float = clock.tick(constants.FPS) / 1000

    # update game
    game.update(dt)

    # reset virtual canvas
    canvas.fill((0, 0, 0))

    # draw game onto virtual canvas
    game.draw(canvas)

    # scale virtual canvas and draw onto screen
    scaled_surface = pygame.transform.scale(canvas, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_surface, (0, 0))

    # update entire display
    pygame.display.flip()