from enum import Enum
from select_number_players_screen import SelectPlayersScreen
from games import GamePlayInfo
from category import CategoryInfo
from utils_local import Color
from player_name.player_name_entry_screen import PlayerNameEntryScreen
import copy

class InternalState(Enum):
    PLAYER_SELECTION_SCREEN = 0
    CATEGORY_SELECTION_SCREEN = 1
    EXIT = 2

class PlayOptionScreen:
    
    def __init__(self):
        self.init_object = False
        self.state = InternalState.PLAYER_SELECTION_SCREEN
        self.player_names = []
        self.player_name_entry_screen = PlayerNameEntryScreen()
        
    def init_screen(self):
        self.select_player_screen = SelectPlayersScreen()


    def render_screen(self, pygame, screen):
        print("Select the Number of Players Screen")

        if not self.init_object:
            self.init_screen()
            self.init_object = True
        game_info = GamePlayInfo()
        nb_player = self.select_player_screen.render_screen(pygame, screen=screen)
        self.player_names = self.player_name_entry_screen.render_player_name_screen(nb_player)
        category_tmp = ["Math", "Sport", "History", "Movie"]
        colors = [Color.BLUE.value, Color.YELLOW.value, Color.RED.value, Color.GREEN.value]
        categories = []
        for index,category_name in enumerate(category_tmp):
            categories.append(CategoryInfo(name=category_name, color=colors[index]))
        game_info.set_nb_player(nb_player=nb_player)
        game_info.set_categories(categories=categories)
        game_info.set_player_names(player_names=self.player_names)

        return game_info
    
    


            