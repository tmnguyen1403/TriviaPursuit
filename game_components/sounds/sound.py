from utils_local import Color, create_button, is_point_inside_rect
from buttons import Button, ButtonRenderer
import pygame

class Sound:
    def __init__(self, screen) -> None:
        self.init = False
        self.screen = screen
        screen_width, screen_height = self.screen.get_size()
        self.mute_button_rect = (0, screen_height - 50, 150, 50)
        self.muted = 0
        pygame.mixer.init()
        pygame.mixer.music.load("..\\sounds\\background.mp3")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.5)

    def draw(self, engine):
        if not self.init:
            self.button_renderer = ButtonRenderer(engine)
            self.mute_button = create_button(self.mute_button_rect, Color.BLUE.value, "Mute Music",
                                                 Color.BLACK.value)
            self.buttons = [self.mute_button]
            self.font = engine.font.SysFont(None, 24)
            self.init = True

        for button in self.buttons:
            self.button_renderer.draw(self.screen, button=button, font=self.font)

    def handle_click(self, engine):
        mouse_pos = engine.mouse.get_pos()
        if is_point_inside_rect(mouse_pos, self.mute_button_rect):
            if self.muted == 1:
                pygame.mixer.music.set_volume(0.5)
                self.muted = 0
            else:
                pygame.mixer.music.set_volume(0)
                self.muted = 1