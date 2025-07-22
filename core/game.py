import pygame

from ui.window import Window
from windows.titlewindow import TitleWindow

# game manager class
class Game:

    def __init__(self):
        # put these in seperate class
        self.title_font: pygame.font.Font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)
        self.normal_font: pygame.font.Font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 8)

        self.request_quit: bool = False

        self.current_scene: Window = TitleWindow(self)
        self.current_scene.active = True

    def handle_event(self, event: pygame.event.Event):
        self.current_scene.handle_event(event)

    def update(self, dt: float):
        self.current_scene.update(dt)
    
    def draw(self, screen: pygame.Surface):
        self.current_scene.draw(screen)

    def change_scene(self, new_window: Window):
        self.current_scene = new_window

    def quit(self):
        self.request_quit = True