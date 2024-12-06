# item.py

import pygame
from settings import BLUE

class Item:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
