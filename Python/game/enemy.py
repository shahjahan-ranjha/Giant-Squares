# enemy.py

import pygame
import random
from settings import WIDTH, HEIGHT, RED

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = random.randint(2, 4)

    def move(self):
        self.rect.x += random.choice([-self.speed, self.speed])
        self.rect.y += random.choice([-self.speed, self.speed])

        # Keep enemy within screen bounds
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x -= random.choice([-self.speed, self.speed])
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.y -= random.choice([-self.speed, self.speed])

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
