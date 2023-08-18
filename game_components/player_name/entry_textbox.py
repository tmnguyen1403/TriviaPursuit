import pygame
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils_local import Color

class TextBox:
    def __init__(self, x, y, width, height, player_index):
        self.rect = pygame.Rect(x, y, width, height)
        self.player_index = player_index
        self.text = ""
        self.active = False
        self.color_inactive = Color.BLACK.value
        self.color_active = Color.BRIGHT_BLUE.value
        self.color = self.color_inactive
        # Screen dimensions
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 1000

        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # Fonts
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
        txt_surface = self.font.render(self.text, True, self.color)
        self.screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event, player_names):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            player_names[self.player_index] = self.text