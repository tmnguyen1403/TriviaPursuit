class Tile:
    def __init__(self, category, color, rect, type):
        self.category = category
        self.color = color
        self.rect = rect #(x,y,width,height)
        self.type = type #Allows to perform certain action depending on tile
        self.border_info = (2,2, (0,0,0)) #margin_x,margin_y, color, 
    def draw(self, engine, screen):
        x,y,width,height = self.rect
        border_x, border_y, border_color = self.border_info
        inner_x = x + border_x
        inner_y = y + border_y
        inner_width = width - border_x * 2
        inner_height = height - border_y * 2
        engine.draw.rect(screen,border_color,  (x,y,width, height))
        engine.draw.rect(screen, self.color, (inner_x,inner_y,inner_width, inner_height))
