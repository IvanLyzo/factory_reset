import pygame
from enum import Enum

import constants
import utils

from ui.window import Window

class HackState(Enum):
    IN_PROGRESS = 0
    PASSED = 1
    FAILED = 2

class HackWindow(Window):

    def __init__(self):
        super().__init__(40)

        self.state: HackState = HackState.IN_PROGRESS
        self.gen_map()

    def gen_map(self):
        data = utils.load_json("hackmaps")
        self.grid: list[list[int]] = data["maps"][0]        

    def handle_event(self, event: pygame.event.Event):
        pass  # Override in subclass

    def update(self, dt: float):
        pass  # Override in subclass

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rect.x + x * constants.VIRTUAL_TILE, self.rect.y + y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE))