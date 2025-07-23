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

        self.tick_increment: float = 0
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2()

        self.snake: list[pygame.math.Vector2] = []

        self.state: HackState = HackState.IN_PROGRESS
        self.load_data()

    def load_data(self):
        data = utils.load_json("hackmaps")["maps"][0]
        self.grid: list[list[int]] = data["grid"]

        self.spawn: pygame.math.Vector2 = pygame.math.Vector2(data["spawn"][0], data["spawn"][1])
        self.snake.append(self.spawn)

    def handle_event(self, event: pygame.event.Event):
        match event.key:
            case pygame.K_w:
                self.velocity = pygame.math.Vector2(0, -1)
            case pygame.K_a:
                self.velocity = pygame.math.Vector2(-1, 0)
            case pygame.K_s:
                self.velocity = pygame.math.Vector2(0, 1)
            case pygame.K_d:
                self.velocity = pygame.math.Vector2(1, 0)

    def update(self, dt: float):
        self.tick_increment += min(dt, 1 - self.tick_increment)
        if self.tick_increment < 1:
            return
        
        if len(self.snake) < 4:
            self.snake.append(self.spawn)
        
        index = len(self.snake) - 1
        while index > 0:
            print(self.snake[index])
            index -= 1

        self.snake[0] += self.velocity

        self.tick_increment = 0

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(self.rect.left - 2, self.rect.top - 2, self.rect.width + 4, self.rect.height + 4), 2)

        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rect.x + x * constants.VIRTUAL_TILE, self.rect.y + y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE))
        
        for part in self.snake:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.rect.x + part.x * constants.VIRTUAL_TILE, self.rect.y + part.y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE))