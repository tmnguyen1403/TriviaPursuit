import sys
import os

from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from utils_local import is_point_inside_rect
import pygame
import webbrowser
from games import GameState


class ButtonText(Enum):
    TWO_PLAYER = "2 Players"
    THREE_PLAYER = "3 Players"
    FOUR_PLAYER = "4 Players"

class SelectPlayersScreen:
    def __init__(self):
        self.init_object = False
        self.buttons = {}
    
    def set_nb_player(self, nb_players: int):
        self.nb_players = nb_players

    def init_screen(self, screen):
        screen_width, screen_height = screen.get_size()
        self.text_color = Color.BLACK.value
        pygame.font.init()
        font = pygame.font.SysFont(None, 60)
        # Clear the screen
        screen.fill(Color.WHITE.value)

        # Draw the welcome message
        welcome_text = font.render("Select Number of Players", True, Color.BLACK.value)
        screen.blit(welcome_text, (screen_width // 2 - welcome_text.get_width() // 2, 150))

        self.player_options = {2: ButtonText.TWO_PLAYER, 3: ButtonText.THREE_PLAYER, 4: ButtonText.FOUR_PLAYER}
        
        # Set up button positions on the screen
        two_player_button_rect = (screen_width // 2 - 150, 300, 300, 50)
        three_player_button_rect = (screen_width // 2 - 150, 400, 300, 50)
        four_player_button_rect = (screen_width // 2 - 150, 500, 300, 50)
        self.button_rect = {2: two_player_button_rect, 3: three_player_button_rect, 4: four_player_button_rect,} 
    
    def create_button(self, rect, button_color, text:ButtonText,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text.value, text_color, action)
        self.buttons[text] = button
        return button

    def render_screen(self, pygame, screen):
        print("Select the Number of Players Screen")
        
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
        running = True

        #display button options
        
        for nb_player, button_text in self.player_options.items():
            button = self.create_button(self.button_rect[nb_player], button_color=Color.BLACK.value,text=button_text, action=lambda n=nb_player: self.set_nb_player(n))
            self.button_renderer.draw(screen=screen,button=button, font=self.font)
        while  running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    # sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in self.buttons.values():
                            if is_point_inside_rect(mouse_pos,button.get_rect()):
                                button.on_click()
                                print("Nb of player: ", self.nb_players)
                                running = False
            pygame.display.flip()
        return self.nb_players