import sys
import pygame

from constants import *

from core.game import Game
from map.tile import TileType

pygame.init()

canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Factory Reset")

TileType.load_images()

clock = pygame.time.Clock()
game = Game()

def quit_game():
    pygame.quit()
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        game.handle_event(event)
        
    if game.request_quit:
        quit_game()
        
    dt = clock.tick(FPS) / 1000

    # update
    game.update(dt)

    # draw
    canvas.fill((0, 0, 0))
    game.draw(canvas)

    scaled_surface = pygame.transform.scale(canvas, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()