from interface import TilePublisher
from typing import List, Tuple
from utils import is_point_inside_rect
'''
Applying Observer (Publisher Subscriber pattern) to handle category from gameboard

'''
class Gameboard(TilePublisher):
    def __init__(self, tile_info, move_calculator: 'MoveCalculator'):
        board_matrix, tile_map, tile_objects = tile_info
        self.titles = tile_objects
        self.tile_map = tile_map
        self.subscribers = list()
        self.category = None
        self.matrix = board_matrix
        self.move_calculator = move_calculator
        self.center = (len(board_matrix)//2, len(board_matrix[0])//2)
        self.candidate_tiles = dict()
        self.candidate_color = (125,125,125)
        self.selected_tile = None
        self.matrix_tile_position = None

    def get_center(self):
        return self.center
    
    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            index = self.subscribers.index(subscriber)
            self.subscribers.pop(index)

    def move(self, mouse_pos):
        has_move = False
        print("Calling move in gameboard")
        for move, tile in self.candidate_tiles.items():
            if is_point_inside_rect(mouse_pos, tile.get_rect()):
                print(f"Tile at {move} is selected. Updating player position")
                self.category = tile.get_category()
                has_move = True
                self.selected_tile = tile
                self.matrix_tile_position = move
                break
        if self.selected_tile:
            self.notify()
            self.reset_tiles()
        return has_move

    def get_selected_tile(self):
        return self.selected_tile
    
    def reset_tiles(self):
        for move, tile in self.candidate_tiles.items():
            tile.reset()
        self.candidate_tiles = dict()
        #self.selected_tile = None
        self.matrix_tile_position = None

    def get_possible_moves(self, player_pos, dice_value):
        possible_moves = self.move_calculator.next_moves(self.matrix, player_pos, dice_value)
        for move in possible_moves:
            tile = self.tile_map[move]
            tile.set_move_candidate(candidate_color = self.candidate_color)
            self.candidate_tiles[move] = tile
        return possible_moves
        
    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.selected_tile, self.matrix_tile_position)

    def get_tile_map(self):
        return self.tile_map
    
    # Use for easy debugging
    def move_debug(self):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                move = (row,col)
                if self.tile_map.get(move, None) is None:
                    continue
                tile = self.tile_map[move]
                #tile.set_move_candidate(candidate_color = self.candidate_color)
                self.candidate_tiles[move] = tile