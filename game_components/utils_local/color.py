from enum import Enum

class Color(Enum):
    #R,G,B,Alpha
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    GREEN = (0, 255, 0, 255)
    BLUE = (0,0,255, 255)
    YELLOW = (255,255,0, 255)
    RED =(255,0,0, 255)
    SPECIAL = (244,88,20, 255)
    DEFAULT_SCREEN = (125,125,125, 255)
    GRAY = (125,125,125, 255)
    ORANGE = (255,165,0, 255)
    MAGENTA = (255, 0, 255, 255)
    CYAN = (0, 255, 255, 255)
    HIGHLIGHT_COLOR = (200, 45, 200, 255)
    BRIGHT_BLUE = (0, 150, 255, 255)
