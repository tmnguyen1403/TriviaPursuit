from enum import Enum
from utils_local import Color
class TileType(Enum):
    NORMAL=1
    HEADQUATER=2
    FREEROLL=3
    TRIVIA_COMPUTE=4 
class Tile:
    def __init__(self, category, color, rect, type):
        self.category = category
        self.origin_color = color
        self.color = color
        self.rect = rect #(x,y,width,height)
        self.type = type #Allows to perform certain action depending on tile
        self.border_info = (2,2, (0,0,0)) #margin_x,margin_y, color,

    def get_rect(self):
        return self.rect
    
    def get_category(self):
        return self.category
    
    def get_category_color(self):
        return self.origin_color
    
    def get_type(self):
        return self.type
    
    def set_type(self, tile_type):
        self.type = tile_type

    def draw(self, engine, screen):
        x,y,width,height = self.rect
        border_x, border_y, border_color = self.border_info
        inner_x = x + border_x
        inner_y = y + border_y
        inner_width = width - border_x * 2
        inner_height = height - border_y * 2
        engine.draw.rect(screen,border_color,  (x,y,width, height))
        engine.draw.rect(screen, self.color, (inner_x,inner_y,inner_width, inner_height))

        # Draw headquater symbol
        if self.type == TileType.HEADQUATER:
            font = engine.font.Font(None, 32)
            hq_text = font.render("HQ", True, Color.BLACK.value, None)
            screen.blit(hq_text, (inner_x + inner_width//3,inner_y+inner_height//3))

        # Draw trivial compute symbol
        if self.type == TileType.TRIVIA_COMPUTE:
            font = engine.font.Font(None, 32)
            hq_text = font.render("TC", True, Color.BLACK.value, None)
            screen.blit(hq_text, (inner_x + inner_width // 3, inner_y + inner_height // 3))

    def set_move_candidate(self, candidate_color = (125,125,125)):
        #print("Tile is move candidate\n")
        self.origin_color = self.color
        self.color = candidate_color
    def reset(self):
        self.color = self.origin_color
    