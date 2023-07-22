from enum import Enum

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    RED =(255,0,0)
    SPECIAL = (244,88,20)
    DEFAULT_SCREEN = (125,125,125)