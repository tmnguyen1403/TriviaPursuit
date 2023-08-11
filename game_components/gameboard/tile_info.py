from .tile_type import TileType

class TileInfo:
    def __init__(self, color: 'Color', tile_type: TileType):
        self.color = color
        self.type = tile_type
        
    def get_color(self):
        return self.color
    
    def get_type(self):
        return self.type 
    
    def set_color(self, color):
        self.color = color
    
    def set_type(self, tile_type):
        self.type = tile_type