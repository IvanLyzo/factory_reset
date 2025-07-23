import pygame

from ui.window import Window
from windows.titlewindow import TitleWindow

# game manager class
class Game:

    def __init__(self):
        self.request_quit: bool = False # flag to request game shutdown

        # set initial window to title screen
        self.current_window: Window = TitleWindow(self)
        self.current_window.active = True

    # handle event input (passed from main loop)
    def handle_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return

        self.current_window.handle_event(event)

    # update current window
    def update(self, dt: float):
        self.current_window.update(dt)
    
    # draw current window
    def draw(self, screen: pygame.Surface):
        self.current_window.draw(screen)

    # switch to new window
    def change_window(self, new_window: Window):
        self.current_window = new_window

    # request to quit game
    def quit(self):
        self.request_quit = True