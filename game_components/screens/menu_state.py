from enum import Enum

class MenuState(Enum):
    WAIT_SELECTION=0
    PLAY_GAME=1
    QUESTION_CENTER=2
    OPTIONS=3
    EXIT=10