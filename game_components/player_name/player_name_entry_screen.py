import pygame
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils_local import Color
from .submit_button import Button
from .entry_textbox import TextBox

class PlayerNameEntryScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 1000

        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Trivia Pursuit - Player Names")

        # Fonts
        self.font = pygame.font.Font(None, 36)


    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def render_player_name_screen(self, num_players):
        running = True
        player_names = [[] for _ in range(num_players)]
        text_boxes = [TextBox(540, 258 + i * 70, 200, 32, i) for i in range(num_players)]
        submit_button = Button(530, 600, 110, 45, "SUBMIT")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for text_box in text_boxes:
                    text_box.handle_event(event, player_names)
                if event.type == pygame.MOUSEBUTTONUP:
                    if submit_button.rect.collidepoint(event.pos):
                        running = False

            self.screen.fill(Color.WHITE.value)

            for i, text_box in enumerate(text_boxes):
                self.draw_text(f"Player {i + 1}:", Color.BLACK.value, 420, (260 + i * 70))
                text_box.draw()
 
            submit_button.draw()

            text_content = "Enter Player Names"
            text_surface = self.font.render(text_content, True, Color.BLACK.value)
            text_rect = text_surface.get_rect()
            text_rect.center = (self.SCREEN_WIDTH // 2, (self.SCREEN_HEIGHT // 2) - 325)
            self.screen.blit(text_surface, text_rect)

            line_start = (text_rect.left, text_rect.bottom + 5)
            line_end = (text_rect.right, text_rect.bottom + 5)
            pygame.draw.line(self.screen, Color.BLACK.value, line_start, line_end, 2)

            pygame.display.flip()

        return player_names



    

