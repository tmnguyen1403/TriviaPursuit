from typing import List
from interface import TileSubscriber
class PlayerManager(TileSubscriber):
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, players: List['Player']) -> None:
        self.test = 0
        self.players = players
        self.current_player = players[0]
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
    