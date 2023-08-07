from .tile import Tile, TileType

class TileGenerator:
    def __init__(self, categories, tile_matrix, head_quater_map, trivial_compute_map, normal_info, special_info, board_rect):
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
        self.normal_info = normal_info
        self.special_info = special_info
        self.board_rect = board_rect
        self.head_quater_map = head_quater_map
        self.trivial_compute_map = trivial_compute_map
    
    def generate(self):
        nb_rows = len(self.tile_matrix) + 1
        nb_cols = len(self.tile_matrix[0]) + 1
        x_start,y_start,board_width,board_height = self.board_rect
        tile_width = board_width // nb_cols
        tile_height = board_height // nb_rows
        border_size = tile_width // nb_cols
        tiles = []
        tile_map = dict() #Use to lookup tile object based on its position in the matrix
        EMPTY_CELL=-10
        for row in range(nb_rows - 1):
            for col in range(nb_cols - 1):
                index = self.tile_matrix[row][col]
                if index == EMPTY_CELL:
                    continue
                x = x_start + (col * tile_width) + ((col+1) * border_size)
                y = y_start + (row * tile_height) + ((row+1) * border_size)
                # Border Drawing
                # inner_x = x + border_size
                # inner_y = y + border_size
                # inner_size = square_size - border_size * 2
                tile_rect = (x,y,tile_width,tile_height)
                info = self.special_info
                category = None
                if index >= 0:
                    info = self.normal_info
                    category_info = self.categories[index]
                    category = category_info.get_name()
                color,tile_type = info[index].get_color(),info[index].get_type()
                if (row,col) in self.head_quater_map:
                    tile_type = TileType.HEADQUATER
                tile = Tile(category=category, color=color,rect=tile_rect, type = tile_type)
                tiles.append(tile)
                tile_map[(row,col)] = tile
                
        return tiles, tile_map
    
