from .tile_type import TileType
from utils_local import Color

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

        #this code to make borders should be obsolete
        #border_x, border_y, border_color = self.border_info
        #inner_x = x + border_x
        #inner_y = y + border_y
        #inner_width = width - border_x * 2
        #inner_height = height - border_y * 2
       
        engine.draw.rect(screen, self.color, self.rect)

        # Draw headquater symbol
        if self.type == TileType.HEADQUARTER:
            font = engine.font.Font(None, 32)
            hq_text = font.render("HQ", True, Color.BLACK.value, None)
            screen.blit(hq_text, (x + width//3, y + height//3))

        # Draw trivial compute symbol
        if self.type == TileType.TRIVIA_COMPUTE:
            font = engine.font.Font(None, 32)
            hq_text = font.render("TC", True, Color.BLACK.value, None)
            screen.blit(hq_text, (x + width // 3, y + height // 3))

    def set_move_candidate(self, candidate_color = (125,125,125)):
        #print("Tile is move candidate\n")
        self.origin_color = self.color
        self.color = candidate_color
    def reset(self):
        self.color = self.origin_color
    