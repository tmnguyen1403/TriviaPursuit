from enum import Enum
from select_number_players import SelectPlayersScreen
class InternalState(Enum):
    PLAYER_SELECTION_SCREEN = 0
    CATEGORY_SELECTION_SCREEN = 1
    EXIT = 2

class PlayOptionScreen:
    def __init__(self):
        self.init_object = False
        self.state = InternalState.PLAYER_SELECTION_SCREEN
        
    def init_screen(self, screen):
        self.select_player_screen = SelectPlayersScreen()

    def render_screen(self, pygame, screen, game_manager):
        print("Select the Number of Players Screen")
        
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
        running = True
        self.game_manager = game_manager
        nb_player = self.select_player_screen.render_screen(pygame, screen=screen)
        print(f"PlayOptionScreen, nb_player: {nb_player}")
        return nb_player
        # while  running or self.state() != InternalState.EXIT:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #             pygame.quit()
        #     self.select_player_screen.render_screen(pygame, screen=screen)
            
            