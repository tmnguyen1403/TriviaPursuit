from .player import Player
from typing import List
from dice.dice_manager import DiceManager
class PlayerManager:
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, players: List[Player]) -> None:
        self.test = 0
        self.players = players
        self.current_player = None
    
    def move(self, dice_manager: DiceManager):
        dice_value = dice_manager.dice.get_value()
        print("inside player manager: ", dice_value)
        return None