from utils_local import Color, is_mac, is_windows
import pygame
import os

#
class IntermediateWinnerScreen:
    def __init__(self, screen, max_display_time_second):
        self.screen = screen
        self.max_display_time_second = max_display_time_second
        self.init = False

    def init_screen(self, screen):
        screen_width, screen_height = screen.get_size()
        self.text_color = Color.BLACK.value
        pygame.font.init()
        font = pygame.font.SysFont(None, 60)
        # Clear the screen
        screen.fill(Color.WHITE.value)
        background_path = ""
        logo_path = ""
        if is_mac():
            background_path = os.path.join("..","..","assets","images","WinnerPage.PNG")
        elif is_windows():
            background_path = os.path.join("assets","images","WinnerPage.PNG")
        background_image = pygame.image.load(background_path) 
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        # Display the background image
        screen.blit(background_image, (0, 0))

    def render_screen(self, engine, screen):
        print("IntermediateWinnerScreen")
        if not self.init:
            self.init_screen(screen=screen)
            self.init = True
        
        running = True
        display = False
        time_pass = 0
        clock = engine.time.Clock()
        while running:
            for event in engine.event.get():
               if event.type == engine.QUIT:
                   running = False
                   break
            if not display:
                engine.display.flip()
                display = True
            else:
                time_pass += clock.tick(60)/1000
                if time_pass > self.max_display_time_second:
                    running = False
                    display = False
                    break
