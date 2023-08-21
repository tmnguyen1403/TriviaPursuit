import sys
import os
import subprocess

# Add Python path to help import
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)

from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from utils_local import is_point_inside_rect, is_mac, is_windows, create_button
from typing import List
import pygame
from player import Player, PlayerManager

class InternalState(Enum):
    PROMPT_OPTION_SELECTION = 0
    WAIT_OPTION_SELECTION = 1
    UPDATE = 2
    EXIT = 3

class ButtonText(Enum):
    RETURN="Quit"

class FinalWinnerScreen:
    def __init__(self):
        self.font = None
        self.button_renderer = None
        self.quit_rect = None
        self.instruction_label_position = None
        self.text_color = None
        self.button_position = None
        self.state = InternalState.PROMPT_OPTION_SELECTION
        self.init_object = False
        self.buttons = {}
        self.player_manager = None

    def init_screen(self, screen, pygame):
        screen_width, screen_height = screen.get_size()
        self.text_color = Color.WHITE.value
        self.instruction_label_position = (screen_width // 2, screen_height//4, 100, 50)

        background_path = ""
        if is_mac():
            background_path = os.path.join("..", "..", "assets", "images", "background.jpg")
        elif is_windows():
            background_path = os.path.join("..", "..", "assets", "images", "background.jpg")
        background_image = pygame.image.load(background_path)
        self.background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

        # Button settings
        self.return_rect = (screen_width // 2 - 150, screen_height - screen_height//5, 300, 50)
        return_button = create_button(self.return_rect, button_color=Color.BLUE.value, text=ButtonText.RETURN.value,
                                           action=lambda: self.set_state(InternalState.EXIT))
        self.buttons[ButtonText.RETURN.value] = return_button

    def draw(self,screen):
        screen.blit(self.background_image, (0, 0))
        # Button render
        for button in self.buttons.values():
            self.button_renderer.draw(screen=screen, button=button, font=self.font)
        self.draw_label(screen=screen)

    def draw_label(self, screen):
        label_text = 'Winners'
        label_source = self.font.render(label_text, True, self.text_color, None)
        screen.blit(label_source, self.instruction_label_position)

        if self.player_manager and self.player_manager.has_winner():
            winners = self.player_manager.get_winners()
            x,y,width,height = self.instruction_label_position
            for index, player in enumerate(winners):
                current_y = y + (index + 1)*50
                winner_text = player.get_name()
                winner_color = player.get_color()
                winner_source = self.font.render(winner_text, True, winner_color, None)
                screen.blit(winner_source, (x,current_y,width,height))

    def set_state(self, new_state: 'InternalState'):
        print(f"Current SelectScreen state: {self.state}")
        self.state = new_state
        print(f"New SelectScreen state: {self.state}")

    def render_screen(self, pygame, screen, player_manager):
        self.set_state(InternalState.PROMPT_OPTION_SELECTION)
        if not self.init_object:
            self.init_screen(screen=screen, pygame=pygame)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
            self.player_manager = player_manager
  
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.state == InternalState.WAIT_OPTION_SELECTION:
                            
                            buttons = self.buttons
                            for button in buttons:
                                if is_point_inside_rect(mouse_pos, buttons[button].get_rect()):
                                    buttons[button].on_click()

            if self.state == InternalState.PROMPT_OPTION_SELECTION or self.state == InternalState.UPDATE:
                self.draw(screen=screen)
                self.set_state(InternalState.WAIT_OPTION_SELECTION)
            elif self.state == InternalState.EXIT:
                running = False

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    # Set screen size
    screen_width = 1200
    screen_height = 1000
    display_index = 0
    screen = pygame.display.set_mode(size=(screen_width, screen_height), display=display_index)
    final_screen = FinalWinnerScreen()
    #
    players = []
    player_colors = {1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value}
    nb_player = 4
    player_names = ["Tom", "Nic", "Ada", "Luxio"]
    for i in range(nb_player):
        player_info = {"position": (0, 0), "name": player_names[i], "token": None, "score": [], "color": player_colors[i + 1]}
        players.append(Player(player_info))
    player_manager = PlayerManager(players=players)
    player_manager.winners = [0,1,2,3]
    final_screen.render_screen(pygame, screen=screen, player_manager=player_manager)
