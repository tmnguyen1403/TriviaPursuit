from typing import List
from interface import TileSubscriber
import .score_box import Score_box
class PlayerManager(TileSubscriber):
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, players: List['Player']) -> None:
        self.test = 0
        self.players = players
        self.current_player = players[0]
        self.current_index = 0
        self.player_scores = []
    def init_player_score(self, cat_colors):
        for player_id in range(list(self.players)):
            self.player_scores[player_id] = Score_box(rect, cat_colors)
    def next_player(self):
        next_index = (self.current_index + 1)%len(self.players)
        self.current_player = self.players[next_index]
        self.current_index = next_index
        print(f"Next player index: {self.current_index}")
    def update(self, tile ,matrix_position):
        print("Update current player position")
        self.current_player.update(matrix_position)
        
    def update_all(self,new_position):
        for player in self.players:
            player.update(new_position)
    def get_current_player(self):
        return self.current_player
    def get_current_player_position(self):
        return self.current_player.get_position()
    def move(self, dice_manager: 'DiceManager'):
        dice_value = dice_manager.dice.get_value()
        print("inside player manager: ", dice_value)
        return None
    def get_players(self):
        return self.players
    