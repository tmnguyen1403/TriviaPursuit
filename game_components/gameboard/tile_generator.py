from .tile import Tile

class TileGenerator:
    def __init__(self, categories, tile_matrix, colors, tile_types, board_rect):
        """_summary_

        Args:
            categories (dict[int, string]): 
            tile_matrix (List[List]): tile arrangement on the board
            colors (dict[int,color]): tile color for different categories 
            tile_types (dict[int, action_type]): tiles might have different action types
            board_rect (tuple[x,y,width,height]): starting position of the board 
        """        
        self.categories = categories
        self.tile_matrix = tile_matrix
        self.colors = colors
        self.tile_types = tile_types
        self.board_rect = board_rect
    
    def generate(self):
        nb_rows = len(self.tile_matrix)
        nb_cols = len(self.tile_matrix[0])
        x_start,y_start,board_width,board_height = self.board_rect
        tile_width = board_width // nb_cols
        tile_height = board_height // nb_rows
        #border_size = 5
        tiles = []
        for row in range(nb_rows):
            for col in range(nb_cols):
                x = x_start + col * tile_width
                y = y_start + row * tile_height
                # Border Drawing
                # inner_x = x + border_size
                # inner_y = y + border_size
                # inner_size = square_size - border_size * 2
                index = self.tile_matrix[row][col]
                if index >= 0:
                    tile_rect = (x,y,tile_width,tile_height)
                    tile = Tile(category=self.categories[index], color=self.colors[index],rect=tile_rect, type = self.tile_types[index])
                    tiles.append(tile)
        return tiles
    
