from enum import Enum

class GameState(Enum):
    WAIT_ROLL = 0
    MOVE_SELECTION = 1
    QUESTION_SELECTION = 2
    QUESTION_ANSWER = 3
    QUESTION_CORRECT = 4
    PLAYER_SELECTION = 5
class GameManager:
    def __init__(self):
        self.current_state = GameState.WAIT_ROLL
    def next_state(self):
        print("current state: ", self.current_state)
        self.current_state = GameState(self.current_state.value + 1)
        print("new state: ", self.current_state)
    def get_state(self):
        return self.current_state