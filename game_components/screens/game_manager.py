from enum import Enum

class GameState(Enum):
    WAIT_ROLL = 0
    MOVE_SELECTION = 1
    QUESTION_SELECTION = 2
    ACCEPT_ANSWER = 3
    REJECT_ANSWER = 4
    PLAYER_SELECTION = 5
    TRIVIAL_COMPUTE_SELECTION = 6
class GameManager:
    def __init__(self):
        self.current_state = GameState.WAIT_ROLL
    def next_state(self):
        print("current state: ", self.current_state)
        self.current_state = GameState(self.current_state.value + 1)
        print("new state: ", self.current_state)
    def set_state(self, state):
        self.current_state = state
    def accept(self):
        print("Accept state: ")
        self.current_state = GameState.ACCEPT_ANSWER
    def reject(self):
        print("Reject state: ")
        self.current_state = GameState.REJECT_ANSWER
    def reset(self):
        self.current_state = GameState.WAIT_ROLL
    def get_state(self):
        return self.current_state