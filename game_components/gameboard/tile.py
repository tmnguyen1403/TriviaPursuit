class Tile:
    def __init__(self, category, color, rect, type):
        self.category = category
        self.color = color
        self.rect = rect #(x,y,width,height)
        self.type = type #Allows to perform certain action depending on tile
