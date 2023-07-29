import sys
from enum import Enum
from utils import Color
from buttons import Button, ButtonRenderer
from utils import is_point_inside_rect
import pygame
import webbrowser
from game_manager import GameState

class ButtonText(Enum):
    PLAY = "Play"
    QUESTION_CENTER = "Question Center"
    QUIT = "Quit"

class LandingScreen:
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
        welcome_text = font.render("Trivial Compute", True, Color.BLACK.value)
        screen.blit(welcome_text, (screen_width // 2 - welcome_text.get_width() // 2, 150))

        # Draw the buttons
        self.play_button_rect = (screen_width // 2 - 150, 300, 300, 50)
        self.questionManage_button_rect = (screen_width // 2 - 150, 400, 300, 50)
        self.quit_button_rect = (screen_width // 2 - 150, 500, 300, 50)
        
        self.button_labels = [ButtonText.PLAY, ButtonText.QUESTION_CENTER, ButtonText.QUIT]
    
    def create_button(self, rect, button_color, text:ButtonText,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text.value, text_color, action)
        self.buttons[text] = button
        return button
        # self.button_renderer.add_button(button)

    def set_manager_state(self, game_state : 'GameState'):
        self.game_manager.set_state(game_state)

    def render_screen(self, pygame, screen, game_manager, question):
        print("Landing Screen")
        
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
        running = True
        self.game_manager = game_manager

        #display button options
        play_button = self.buttons.get(ButtonText.PLAY, None)
        if play_button is None:
            play_button = self.create_button(self.play_button_rect, button_color=Color.BLACK.value,text=ButtonText.PLAY, action=lambda: self.set_manager_state(GameState.WAIT_ROLL))
        self.button_renderer.draw(screen=screen,button=play_button, font=self.font)

        questionManager_button = self.buttons.get(ButtonText.QUESTION_CENTER, None)
        if questionManager_button is None:
            questionManager_button = self.create_button(self.questionManage_button_rect, button_color=Color.BLACK.value,text=ButtonText.QUESTION_CENTER, action=lambda:webbrowser.open_new_tab("http://localhost:3000"))
        self.button_renderer.draw(screen=screen,button=questionManager_button, font=self.font)
        quit_button = self.buttons.get(ButtonText.QUIT, None)
        if quit_button is None:
            quit_button = self.create_button(self.quit_button_rect, button_color=Color.BLACK.value,text=ButtonText.QUIT, action=lambda:sys.exit())
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
