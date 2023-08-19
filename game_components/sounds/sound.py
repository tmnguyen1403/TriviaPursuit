from utils_local import Color, create_button, is_point_inside_rect, is_mac, is_windows
from buttons import Button, ButtonRenderer
import pygame
import os


class Sound:
    def __init__(self, screen) -> None:
        self.init = False
        self.screen = screen
        screen_width, screen_height = self.screen.get_size()
        self.label_position = (screen_width // 2 - 150, 420)
        self.copyright_label_position = (screen_width // 2 + 160, 420)
        self.low_button_rect = (screen_width // 2 - 50, 400, 50, 50)
        self.med_button_rect = (screen_width // 2, 400, 50, 50)
        self.high_button_rect = (screen_width // 2 + 50, 400, 50, 50)
        self.mute_button_rect = (screen_width // 2 + 100, 400, 50, 50)
        self.muted = 0
        if is_mac():
            self.sound_title_path = os.path.join("..","..","assets", "audios", "title.mp3")
            self.sound_background_path = os.path.join("..","..","assets", "audios", "background.mp3")
        elif is_windows():
            self.sound_title_path = os.path.join("..", "..", "assets", "audios", "title.mp3")
            self.sound_background_path = os.path.join("..", "..", "assets", "audios", "background.mp3")
        self.text_color = Color.WHITE.value
        self.current_volume = 0.6
        pygame.mixer.init()
        pygame.mixer.music.stop()

    def draw(self, engine):
        self.button_renderer = ButtonRenderer(engine)
        self.low_button = create_button(self.low_button_rect, Color.GREEN.value, "Low",
                                            Color.BLACK.value)
        self.med_button = create_button(self.med_button_rect, Color.BLUE.value, "Med",
                                            Color.BLACK.value)
        self.high_button = create_button(self.high_button_rect, Color.RED.value, "High",
                                             Color.BLACK.value)
        self.mute_button = create_button(self.mute_button_rect, Color.MAGENTA.value, "Mute",
                                             Color.BLACK.value)
        self.buttons = [self.low_button, self.med_button, self.high_button, self.mute_button]
        self.font = engine.font.SysFont(None, 24)

        label_source = self.font.render('Music Vol: ', True, self.text_color, None)
        self.screen.blit(label_source, self.label_position)

        copyright_label_source = self.font.render('Music from https://www.zapsplat.com', True, self.text_color, None)
        self.screen.blit(copyright_label_source, self.copyright_label_position)

        for button in self.buttons:
            self.button_renderer.draw(self.screen, button=button, font=self.font)

    def play(self, song):
        if song == 'title':
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_title_path)
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(self.current_volume)
        elif song == 'background':
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_background_path)
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(self.current_volume)
        else:
            print('Invalid song')

    def stop(self):
        pygame.mixer.music.stop()

    def handle_click(self, engine):
        mouse_pos = engine.mouse.get_pos()
        if is_point_inside_rect(mouse_pos, self.mute_button_rect):
            if self.muted == 1:
                pygame.mixer.music.set_volume(self.current_volume)
                self.muted = 0
            else:
                pygame.mixer.music.set_volume(0)
                self.muted = 1
        if is_point_inside_rect(mouse_pos, self.low_button_rect):
            self.current_volume = 0.3
            pygame.mixer.music.set_volume(self.current_volume)
            self.muted = 0
        if is_point_inside_rect(mouse_pos, self.med_button_rect):
            self.current_volume = 0.6
            pygame.mixer.music.set_volume(self.current_volume)
            self.muted = 0
        if is_point_inside_rect(mouse_pos, self.high_button_rect):
            self.current_volume = 1.0
            pygame.mixer.music.set_volume(self.current_volume)
            self.muted = 0
