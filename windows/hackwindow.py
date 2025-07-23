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
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(1, 0)

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
        # increment timer and return if not enough time has passed
        self.tick_increment += dt
        if self.tick_increment < 0.5:
            return

        # grow snake outward from spawn until it has 4 segments
        if len(self.snake) < 4:
            self.snake.append(self.spawn.copy())

        # allow movement and collisions once fully formed
        else:
            # shift tail segments toward head
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i] = self.snake[i - 1].copy()

            # update head position based on velocity
            self.snake[0] += self.velocity

            # get tile coordinates for head
            head_x, head_y = int(self.snake[0].x), int(self.snake[0].y)

            # check for out-of-bounds
            if head_x < 0 or head_y < 0 or head_y >= len(self.grid) or head_x >= len(self.grid[head_y]):
                self.state = HackState.FAILED
                return

            # check tile collision
            if 0 <= head_y < len(self.grid) and 0 <= head_x < len(self.grid[head_y]):
                tile = self.grid[head_y][head_x]
                if tile == 1:
                    self.state = HackState.FAILED
                elif tile == 2:
                    self.state = HackState.PASSED

            # check self-collision
            for i in range(1, len(self.snake)):
                if self.snake[0] == self.snake[i]:
                    self.state = HackState.FAILED
                    break

        self.tick_increment = 0

    def draw(self, screen: pygame.Surface):
        # background and border
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(self.rect.left - 2, self.rect.top - 2, self.rect.width + 4, self.rect.height + 4), 2)

        # draw grid tiles
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rect.x + x * constants.VIRTUAL_TILE, self.rect.y + y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE))
                elif val == 2:
                    pygame.draw.rect(screen, (0, 200, 255), pygame.Rect(self.rect.x + x * constants.VIRTUAL_TILE, self.rect.y + y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE))

        # draw snake body
        for i in range(len(self.snake)):
            part = self.snake[i]
            if i == 0:
                color = (255, 0, 0)  # head
            else:
                color = (0, 255, 0)  # body

            pygame.draw.rect(screen, color, pygame.Rect(self.rect.x + part.x * constants.VIRTUAL_TILE, self.rect.y + part.y * constants.VIRTUAL_TILE, constants.VIRTUAL_TILE, constants.VIRTUAL_TILE))