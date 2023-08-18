import pygame
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils_local import Color

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = Color.BRIGHT_BLUE.value
        # Screen dimensions
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 1000

        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # Fonts
        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.draw_text(self.text, Color.BLACK.value, self.rect.x + 10, self.rect.y + 10)
