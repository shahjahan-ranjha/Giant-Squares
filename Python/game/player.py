# player.py

import pygame
from settings import PLAYER_SPEED, PLAYER_HEALTH, WIDTH, HEIGHT, GREEN

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Define a green box for the player
        self.health = PLAYER_HEALTH
        self.energy = 100  # Energy starts at max
        self.strength = 10  # Default strength level

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
            self.energy -= 0.1  # Decrease energy when moving
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
            self.energy -= 0.1
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
            self.energy -= 0.1
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED
            self.energy -= 0.1

        # Regenerate energy when not moving
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.energy += 0.05

        # Keep energy within limits
        self.energy = max(0, min(self.energy, 100))

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)  # Draw the player as a green box
