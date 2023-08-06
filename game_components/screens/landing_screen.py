from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from utils_local import is_point_inside_rect
import pygame
import webbrowser
from menu_state import MenuState

class ButtonText(Enum):
    PLAY = "Play"
    QUESTION_CENTER = "Question Center"
    QUIT = "Quit"

class LandingScreen:
    def __init__(self):
        self.init_object = False
        self.buttons = {}
        self.menu_state = None
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
        play_button_rect = (screen_width // 2 - 150, 300, 300, 50)
        question_center_button_rect = (screen_width // 2 - 150, 400, 300, 50)
        quit_button_rect = (screen_width // 2 - 150, 500, 300, 50)
        
        self.button_labels = [ButtonText.PLAY, ButtonText.QUESTION_CENTER, ButtonText.QUIT]
        self.button_infos = {ButtonText.PLAY: (play_button_rect, MenuState.PLAY_GAME), ButtonText.QUESTION_CENTER: (question_center_button_rect, MenuState.QUESTION_CENTER),  ButtonText.QUIT: (quit_button_rect, MenuState.EXIT)}

    def create_button(self, rect, button_color, text:ButtonText,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text.value, text_color, action)
        self.buttons[text] = button
        return button

    def set_mennu_state(self, state : MenuState):
        self.menu_state = state

    def render_screen(self, pygame, screen):
        print("Landing Screen")
        
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)

        #display button options
        for button_text, button_detail in self.button_infos.items():
            rect, menu_state = button_detail
            button = self.create_button(rect, button_color=Color.BLACK.value,text=button_text, action=lambda state=menu_state: self.set_mennu_state(state))
            self.button_renderer.draw(screen=screen,button=button, font=self.font)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for button_text, button in self.buttons.items():
                            if is_point_inside_rect(mouse_pos,button.get_rect()):
                                button.on_click()
                                return self.menu_state
            pygame.display.flip()
