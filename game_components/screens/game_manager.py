from enum import Enum

class GameState(Enum):
    WAIT_ROLL = 0
    MOVE_SELECTION = 1
    QUESTION_SELECTION = 2
    WAIT_PLAYER_ANSWER = 3
    #QUESTION_REVEAL = 4
    ANSWER_REVEAL = 4
    PLAYER_VOTE = 5
    #QUESTION_CORRECT = 6
    PLAYER_SELECTION = 6
class GameManager:
    def __init__(self):
        self.current_state = GameState.WAIT_ROLL
    def next_state(self):
        print("current state: ", self.current_state)
        self.current_state = GameState(self.current_state.value + 1)
        print("new state: ", self.current_state)
    def reset(self):
        self.current_state = GameState.WAIT_ROLL
    def get_state(self):
        return self.current_state