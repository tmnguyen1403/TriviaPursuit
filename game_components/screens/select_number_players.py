import sys
from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from utils_local import is_point_inside_rect
import pygame
import webbrowser
from game_manager import GameState

class ButtonText(Enum):
    TWO_PLAYER = "2 Players"
    THREE_PLAYER = "3 Players"
    FOUR_PLAYER = "4 Players"

class SelectPlayersScreen:
    def __init__(self):
        self.init_object = False
        self.buttons = {}
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

        # Draw the buttons
        self.play_button_rect = (screen_width // 2 - 150, 300, 300, 50)
        self.questionManage_button_rect = (screen_width // 2 - 150, 400, 300, 50)
        self.quit_button_rect = (screen_width // 2 - 150, 500, 300, 50)
        
        self.button_labels = [ButtonText.TWO_PLAYER, ButtonText.THREE_PLAYER, ButtonText.FOUR_PLAYER]
    
    def create_button(self, rect, button_color, text:ButtonText,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text.value, text_color, action)
        self.buttons[text] = button
        return button
        # self.button_renderer.add_button(button)

    def set_manager_state(self, game_state : 'GameState'):
        self.game_manager.set_state(game_state)

    def render_screen(self, pygame, screen, game_manager, question):
        print("Select the Number of Players Screen")
        
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
        running = True
        self.game_manager = game_manager

        #display button options
        play_button = self.buttons.get(ButtonText.TWO_PLAYER, None)
        if play_button is None:
            play_button = self.create_button(self.play_button_rect, button_color=Color.BLACK.value,text=ButtonText.TWO_PLAYER, action=None)
        self.button_renderer.draw(screen=screen,button=play_button, font=self.font)

        questionManager_button = self.buttons.get(ButtonText.THREE_PLAYER, None)
        if questionManager_button is None:
            questionManager_button = self.create_button(self.questionManage_button_rect, button_color=Color.BLACK.value,text=ButtonText.THREE_PLAYER, action=None)
        self.button_renderer.draw(screen=screen,button=questionManager_button, font=self.font)
        quit_button = self.buttons.get(ButtonText.FOUR_PLAYER, None)
        if quit_button is None:
            quit_button = self.create_button(self.quit_button_rect, button_color=Color.BLACK.value,text=ButtonText.FOUR_PLAYER, action=None)
        self.button_renderer.draw(screen=screen,button=quit_button, font=self.font)


        while  running or self.game_manager.get_state() == GameState.WAIT_ROLL:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        buttons = [self.buttons[ButtonText.PLAY], self.buttons[ButtonText.QUESTION_CENTER], self.buttons[ButtonText.QUIT]]
                        for button in buttons:
                            if is_point_inside_rect(mouse_pos,button.get_rect()):
                                button.on_click()
                                print(button.text)
                                return
            # if self.game_manager.get_state() == GameState.WAIT_ROLL:
            #     return
            pygame.display.flip()


        
