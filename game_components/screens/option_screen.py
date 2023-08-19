from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from utils_local import is_point_inside_rect, is_mac, is_windows, create_button
import os
from typing import List

class InternalState(Enum):
    PROMPT_OPTION_SELECTION = 0
    WAIT_OPTION_SELECTION = 1
    UPDATE = 2
    EXIT = 3

class ButtonText(Enum):
    RETURN="Return"
class OptionScreen:
    def __init__(self, music_handler):
        self.font = None
        self.button_renderer = None
        self.quit_rect = None
        self.instruction_label_position = None
        self.text_color = None
        self.button_position = None
        self.state = InternalState.PROMPT_OPTION_SELECTION
        self.init_object = False
        self.buttons = {}
        self.music_handler = music_handler

    def init_screen(self, screen, pygame):
        screen_width, screen_height = screen.get_size()
        self.text_color = Color.WHITE.value
        self.instruction_label_position = (screen_width // 2, screen_height//4, 100, 50)

        background_path = ""
        logo_path = ""
        if is_mac():
            background_path = os.path.join("..", "..", "assets", "images", "background.jpg")
            logo_path = os.path.join("..", "..", "assets", "images", "logo.png")
        elif is_windows():
            background_path = os.path.join("..", "..", "assets", "images", "background.jpg")
            logo_path = os.path.join("..", "..", "assets", "images", "logo.png")
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
        label_text = 'Options'
        label_source = self.font.render(label_text, True, self.text_color, None)
        screen.blit(label_source, self.instruction_label_position)

    def set_state(self, new_state: 'InternalState'):
        print(f"Current SelectScreen state: {self.state}")
        self.state = new_state
        print(f"New SelectScreen state: {self.state}")

    def render_screen(self, pygame, screen):
        self.set_state(InternalState.PROMPT_OPTION_SELECTION)
        if not self.init_object:
            self.init_screen(screen=screen, pygame=pygame)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
  
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.state == InternalState.WAIT_OPTION_SELECTION:
                            handled = self.music_handler.handle_click(pygame)
                            if not handled: 
                                buttons = self.buttons
                                for button in buttons:
                                    if is_point_inside_rect(mouse_pos, buttons[button].get_rect()):
                                        buttons[button].on_click()
                            else:
                                self.set_state(InternalState.UPDATE)

            if self.state == InternalState.PROMPT_OPTION_SELECTION or self.state == InternalState.UPDATE:
                self.draw(screen=screen)
                self.music_handler.draw(pygame)
                self.set_state(InternalState.WAIT_OPTION_SELECTION)
            elif self.state == InternalState.EXIT:
                running = False

            pygame.display.flip()
