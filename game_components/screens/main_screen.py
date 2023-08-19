# Set up path to load other modules
# Set up PYTHONPATH
import sys
import os
import subprocess
try:
    import pygame
except Exception as e:
    print("Attemp to install packages")
    subprocess.run(["python3 -m pip install $(cat requirements.txt)"], shell=True)
# Add Python path to help import
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)

# Import dependencies
import pygame
import webbrowser

from landing_screen import LandingScreen
from game_play_screen import GamePlayScreen
from play_option_screen import PlayOptionScreen
from option_screen import OptionScreen
from menu_state import MenuState
from category import CategorySelectionScreen
from sounds import Sound, SoundType

if __name__ == "__main__":
    pygame.init()

    # Set screen size
    screen_width = 1200
    screen_height = 1000
    display_index = 0
    screen = pygame.display.set_mode((screen_width, screen_height), display=display_index)
    desktop_size = pygame.display.get_desktop_sizes()
    display_width, display_height = desktop_size[display_index]
    x = (display_width - screen_width)//2
    y = (display_height - screen_height)//2
    screen_top_left_position = (x,y)

    menu_state = MenuState.WAIT_SELECTION
    running = True
    question_center_url = "http://localhost:3000"
    DEBUG = False
    clock = pygame.time.Clock()

    # Music
    music_handler = Sound(screen, screen_position=screen_top_left_position)
    music_handler.play(SoundType.MENU_MUSIC)

    while menu_state != MenuState.EXIT:
        if menu_state == MenuState.WAIT_SELECTION:
            land_screen = LandingScreen(music_handler)
            menu_state = land_screen.render_screen(pygame, screen=screen)
        if menu_state == MenuState.PLAY_GAME:
            game_play_info = None
            if not DEBUG:
                play_option_screen = PlayOptionScreen()
                game_play_info = play_option_screen.render_screen(pygame, screen=screen)

                category_screen = CategorySelectionScreen(screen=screen)
                selected_categories = category_screen.run(engine=pygame)
                
                game_play_info.set_categories(selected_categories)
            else:
                from games import GamePlayInfo
                game_play_info = GamePlayInfo()
                game_play_info.set_debug()

            music_handler.stop()
            game_play_screen = GamePlayScreen(game_info=game_play_info, music_handler=music_handler)
            game_play_screen.render_screen(pygame, screen=screen)

            music_handler.play(SoundType.MENU_MUSIC)
            menu_state = MenuState.WAIT_SELECTION
        if menu_state == MenuState.OPTIONS:
            option_screen = OptionScreen(music_handler)
            option_screen.render_screen(pygame, screen=screen)
            menu_state = MenuState.WAIT_SELECTION
        if menu_state == MenuState.QUESTION_CENTER:
            webbrowser.open_new_tab(question_center_url)
            menu_state = MenuState.WAIT_SELECTION

    pygame.quit()


