from interface import CategoryPublisher
from .move_calculator import MoveCalculator
from typing import List
'''
Applying Observer (Publisher Subscriber pattern) to handle category from gameboard

'''

class GameBoard(CategoryPublisher):
    def __init__(self, database: 'Database', board_matrix: List[List[int]], cant_move=-1):
        self.titles = list(list())
        self.subscribers = list()
        self.category = None
        self.database = database
        self.matrix = board_matrix
        self.move_calculator = MoveCalculator(cant_move=cant_move)
        self.center = (len(board_matrix)//2, len(board_matrix[0])//2)
    
    def get_center(self):
        return self.center
    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            index = self.subscribers.index(subscriber)
            self.subscribers.pop(index)
    def move(self):
        self.category = "Math"
        self.notify()
    def get_moves(self, player_pos, dice_value):
        possible_moves = self.move_calculator.next_moves(self.matrix, player_pos, dice_value)
        return possible_moves
    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.category)

# if __name__ == "__main__":
#     from question import QuestionManager
#     from database import dummy_database, Database
#     database = dummy_database()
#     board = GameBoard(database)
#     question_manager = QuestionManager(database=database)
#     board.subscribe(question_manager)
#     board.move()
#     board.move()
#     board.move()

