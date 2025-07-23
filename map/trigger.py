import pygame

from collections.abc import Callable

from entities.player import Player

class Trigger:
    def __init__(self, rect: pygame.Rect, on_enter: Callable[[], None]):
        self.rect: pygame.Rect = rect  # Area that defines the trigger's bounds
        self.on_enter: Callable[[], None] = on_enter  # Callback to run when triggered

        self.triggered: bool = False  # Tracks if the player is already in the trigger

    def check(self, player: Player):
        # Check if the player's collision area intersects this trigger
        if self.rect.colliderect(player.collision_rect):
            # If player enters and it hasn't been triggered yet, activate
            if not self.triggered:
                self.on_enter()
                self.triggered = True
        
        # Reset trigger if the player leaves the trigger zone
        else:
            self.triggered = False