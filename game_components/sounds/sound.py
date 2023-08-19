from utils_local import Color, create_button, is_point_inside_rect, is_mac, is_windows
from buttons import Button, ButtonRenderer
import pygame
import os
from utils_local import FileSelection
from .sound_type import SoundType
from enum import Enum
class ButtonText(Enum):
    LOW="Low"
    MED="Med"
    HIGH="High"
    MUTE="Mute"
    MENU="Menu"
    GAME="Game"

class ButtonColor(Enum):
    LOW=Color.GREEN.value
    MED=Color.BLUE.value
    HIGH=Color.RED.value
    MUTE=Color.MAGENTA.value
    MENU=Color.BLUE.value
    GAME=Color.GREEN.value
    DISABLE=Color.GRAY.value

class VolumeLevel(Enum):
    LOW=0.3
    MED=0.6
    HIGH=1.0
    MUTE=0.0
class Sound:
    def __init__(self, screen, screen_position) -> None:
        self.init = False
        self.screen = screen
        self.screen_position = screen_position
        screen_width, screen_height = self.screen.get_size()
        height = screen_height //4 + 100
        self.label_position = (screen_width // 2 - 150, height + 20)
        self.copyright_label_position = (screen_width // 2 + 160, height + 20)
        self.low_button_rect = (screen_width // 2 - 50, height, 50, 50)
        self.med_button_rect = (screen_width // 2, height, 50, 50)
        self.high_button_rect = (screen_width // 2 + 50, height, 50, 50)
        self.mute_button_rect = (screen_width // 2 + 100, height, 50, 50)
        
        self.menu_music_rect = (screen_width // 2 - 150, height + 100, 100, 50)
        self.menu_music_label_rect = (screen_width // 2, height + 100 + 20, 100, 50)
        self.game_music_rect = (screen_width // 2 - 150, height + 200, 100, 50)
        self.game_music_label_rect = (screen_width // 2, height + 200 + 20, 100, 50)

        self.buttons = {}
        self.muted = False
        if is_mac():
            self.sound_menu_path = os.path.join("..","..","assets", "audios", "title.mp3")
            self.sound_game_path = os.path.join("..","..","assets", "audios", "background.mp3")
        elif is_windows():
            self.sound_menu_path = os.path.join("..", "..", "assets", "audios", "title.mp3")
            self.sound_game_path = os.path.join("..", "..", "assets", "audios", "background.mp3")
        self.text_color = Color.WHITE.value
        self.current_volume = VolumeLevel.LOW.value
        pygame.mixer.init()
        pygame.mixer.music.stop()

    def draw(self, engine):
        if len(self.buttons) == 0:
            self.font = engine.font.SysFont(None, 24)

            self.button_renderer = ButtonRenderer(engine)
            low_button = create_button(self.low_button_rect, ButtonColor.DISABLE.value, ButtonText.LOW.value,
                                                Color.BLACK.value)
            med_button = create_button(self.med_button_rect, ButtonColor.DISABLE.value, ButtonText.MED.value,
                                                Color.BLACK.value)
            high_button = create_button(self.high_button_rect, ButtonColor.DISABLE.value, ButtonText.HIGH.value,
                                                Color.BLACK.value)
            mute_button = create_button(self.mute_button_rect, ButtonColor.DISABLE.value, ButtonText.MUTE.value,
                                                Color.BLACK.value)
            # Menu music selection
            menu_music_button = create_button(self.menu_music_rect, Color.BLUE.value, ButtonText.MENU.value,
                                                Color.BLACK.value)
            #Game music selection 
            game_music_button = create_button(self.game_music_rect, Color.GREEN.value, ButtonText.GAME.value,
                                                Color.BLACK.value)
            
            self.buttons[ButtonText.LOW.value] = low_button
            self.buttons[ButtonText.MED.value] = med_button
            self.buttons[ButtonText.HIGH.value] = high_button
            self.buttons[ButtonText.MUTE.value] = mute_button
            self.buttons[ButtonText.MENU.value] = menu_music_button
            self.buttons[ButtonText.GAME.value] = game_music_button
        #Always redraw text

        # Menu Music Text
        track_name = self.sound_menu_path.split(os.path.sep)[-1]
        menu_music_label = self.font.render(track_name, True, self.text_color, None)
        self.screen.blit(menu_music_label, self.menu_music_label_rect)
        
        #Game Music Text
        track_name = self.sound_game_path.split(os.path.sep)[-1]
        game_music_label = self.font.render(track_name, True, self.text_color, None)
        self.screen.blit(game_music_label, self.game_music_label_rect)

        label_source = self.font.render('Music Vol: ', True, self.text_color, None)
        self.screen.blit(label_source, self.label_position)

        # Remove due to unknown copyright
        # copyright_label_source = self.font.render('Music from https://www.zapsplat.com', True, self.text_color, None)
        # self.screen.blit(copyright_label_source, self.copyright_label_position)

        for button in self.buttons.values():
            self.button_renderer.draw(self.screen, button=button, font=self.font)

    def play(self, sound_type:SoundType):
      
        if sound_type == SoundType.MENU_MUSIC:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_menu_path)
        elif sound_type == SoundType.GAME_MUSIC:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound_game_path)            
        else:
            print('Invalid sound type')
            return
        self.playing = sound_type
        pygame.mixer.music.play(-1, 0.0)
        if self.muted:
            print("Warning: Sound speaker is muted. Please unmute to hear")
            pygame.mixer.music.set_volume(VolumeLevel.MUTE.value)
        else:
            pygame.mixer.music.set_volume(self.current_volume)

    def stop(self):
        pygame.mixer.music.stop()

    def handle_click(self, engine):
        if len(self.buttons) == 0:
            return False
        mouse_pos = engine.mouse.get_pos()
        clicked_button = None
        button_text = ""
        for key, button in self.buttons.items():
            rect = button.get_rect()
            if is_point_inside_rect(mouse_pos, rect):
                clicked_button = button
                button_text = key
                break

        if clicked_button is None:
            return False
        
        if button_text == ButtonText.MUTE.value:
            if self.muted:
                pygame.mixer.music.set_volume(self.current_volume)
                self.muted = False
                button.set_color(ButtonColor.DISABLE.value)
            else:
                pygame.mixer.music.set_volume(VolumeLevel.MUTE.value)
                self.muted = True
                button.set_color(ButtonColor.MUTE.value)
            return True
        
        #Handle Volume
        selected_volum_button_text = ""
        if button_text == ButtonText.LOW.value:
            self.current_volume = VolumeLevel.LOW.value
            button.set_color(ButtonColor.LOW.value)
            selected_volum_button_text = ButtonText.LOW.value
        elif button_text == ButtonText.MED.value:
            self.current_volume = 0.6
            button.set_color(ButtonColor.MED.value)
            selected_volum_button_text =  ButtonText.MED.value
        elif button_text == ButtonText.HIGH.value:
            self.current_volume = 1.0
            button.set_color(ButtonColor.HIGH.value)
            selected_volum_button_text =   ButtonText.HIGH.value
        if selected_volum_button_text != "":
            volume_texts = [ButtonText.LOW, ButtonText.MED, ButtonText.HIGH]
            for text in volume_texts:
                if text.value ==  selected_volum_button_text:
                    continue
                button = self.buttons.get(text.value)
                button.set_color(ButtonColor.DISABLE.value)
            if not self.muted:
                pygame.mixer.music.set_volume(self.current_volume)
            return True
        
        # Change menu music
        if button_text == ButtonText.MENU.value:
            self.file_selection = FileSelection(default_sound_dir=self.sound_menu_path)
            music_path = self.file_selection.run(window_pos=self.screen_position)
            if music_path != "":
                self.set_menu_path(music_path)
                if self.playing == SoundType.MENU_MUSIC:
                    self.stop()
                    self.play(SoundType.MENU_MUSIC)
        # Chage game music
        elif button_text == ButtonText.GAME.value:
            self.file_selection = FileSelection(default_sound_dir=self.sound_game_path)
            music_path = self.file_selection.run(window_pos=self.screen_position)
            if music_path != "":
                self.set_game_path(music_path)
                if self.playing == SoundType.GAME_MUSIC:
                    self.stop()
                    self.play(SoundType.GAME_MUSIC)
        return True 
    
    def set_menu_path(self, new_path: str):
        self.sound_menu_path = new_path
    
    def set_game_path(self, new_path: str):
        self.sound_game_path = new_path

