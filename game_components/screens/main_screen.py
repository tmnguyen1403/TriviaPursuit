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
from menu_state import MenuState
from category import CategorySelectionScreen

pygame.init()

# Set screen size
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

menu_state = MenuState.WAIT_SELECTION
running = True
question_center_url = "http://localhost:3000"
DEBUG = False

while menu_state != MenuState.EXIT:
    if menu_state == MenuState.WAIT_SELECTION:
        land_screen = LandingScreen()
        menu_state = land_screen.render_screen(pygame, screen=screen)
    if menu_state == MenuState.PLAY_GAME:
<<<<<<< HEAD
        play_option_screen = PlayOptionScreen()
        game_play_info = play_option_screen.render_screen(pygame, screen=screen)
        #print(f"Play Info {game_play_info}")
        category_screen = CategorySelectionScreen(screen=screen)
        selected_categories = category_screen.run(engine=pygame)
        #print(f"selected category {selected_categories}")
        game_play_info.set_categories(selected_categories)
=======
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
>>>>>>> integration

        game_play_screen = GamePlayScreen(game_info=game_play_info)
        game_play_screen.render_screen(pygame, screen=screen)
        menu_state = MenuState.WAIT_SELECTION
    if menu_state == MenuState.QUESTION_CENTER:
        webbrowser.open_new_tab(question_center_url)
        menu_state = MenuState.WAIT_SELECTION

pygame.quit()


