import pygame

from scenes.menu import MenuScene

class Game:

    def __init__(self):
        self.title_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)
        self.normal_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 8)

        self.request_quit = False

        self.current_scene = MenuScene(self)

    def handle_event(self, event):
        self.current_scene.handle_event(event)

    def update(self, dt):
        self.current_scene.update(dt)
    
    def draw(self, screen):
        self.current_scene.draw(screen)

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def quit(self):
        self.request_quit = True