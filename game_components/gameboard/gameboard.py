from interface import CategoryPublisher
from typing import List, Tuple
from utils import is_point_inside_rect
'''
Applying Observer (Publisher Subscriber pattern) to handle category from gameboard

'''

class Gameboard(CategoryPublisher):
    def __init__(self, database: 'Database', tile_info, move_calculator: 'MoveCalculator'):
        board_matrix, tile_map, tile_objects = tile_info
        self.titles = tile_objects
        self.tile_map = tile_map
        self.subscribers = list()
        self.category = None
        self.database = database
        self.matrix = board_matrix
        self.move_calculator = move_calculator
        self.center = (len(board_matrix)//2, len(board_matrix[0])//2)
        self.candidate_tiles = dict()
        self.candidate_color = (125,125,125)
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
        for move, tile in self.candidate_tiles.items():
            if is_point_inside_rect(mouse_pos, tile.get_rect()):
                print(f"Tile at {move} is selected. Updating player position")
                self.category = tile.get_category()
                has_move = True
                break
        if has_move:
            self.reset_tiles()
            self.notify()
        return has_move

    def reset_tiles(self):
        for move, tile in self.candidate_tiles.items():
            tile.reset()
        self.candidate_tiles = dict()
    def get_possible_moves(self, player_pos, dice_value):
        possible_moves = self.move_calculator.next_moves(self.matrix, player_pos, dice_value)
        for move in possible_moves:
           # print(f"Gameboard move: {move}")
            tile = self.tile_map[move]
            tile.set_move_candidate(candidate_color = self.candidate_color)
            self.candidate_tiles[move] = tile
            #self.tile_map[move].
        return possible_moves
    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.category)

# if __name__ == "__main__":
#     from question import QuestionManager
#     from database import dummy_database, Database
#     database = dummy_database()
#     board = Gameboard(database)
#     question_manager = QuestionManager(database=database)
#     board.subscribe(question_manager)
#     board.move()
#     board.move()
#     board.move()

