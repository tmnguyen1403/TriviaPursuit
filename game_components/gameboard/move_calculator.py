from typing import Dict, List, Optional, Tuple

class MoveCalculator:
    def __init__(self, cant_move):
        self.cant_move = cant_move
        
    def change_cant_move(self, cant_move):
        self.cant_move = cant_move

    def is_out_of_range(self, my_range:Tuple[int,int], position:Tuple[int,int]):
        row, col = position
        max_row, max_col = my_range
        if row < 0 or row >= max_row:
            return True
        if col < 0 or col >= max_col:
            return True
        return False

    def is_movable(self, board_matrix: List[List[int]], position:Tuple[int,int]):
        row, col = position
        max_row, max_col = len(board_matrix), len(board_matrix[0])
        if self.is_out_of_range(my_range=(max_row, max_col), position=position):
            return False
        value = board_matrix[row][col]
        return value != self.cant_move
    
    def next_moves(self, board_matrix: List[List[int]], player_pos:Tuple[int,int], dice_value: int, check_move=True):
        moves = []
        row, col = player_pos
        print(f"player pos: {row},{col}")
        for h in range(dice_value+1):
            v = dice_value - h
            for sign_h in [1,-1]:
                if h == 0 and sign_h == -1:
                    continue
                for sign_v in [1,-1]:
                    if v == 0 and sign_v == -1:
                        continue
                    next_row = row + h*sign_h
                    next_col = col + v*sign_v
                    if not check_move:
                        moves.append((next_row,next_col))
                        continue
                    if  self.is_movable(board_matrix=board_matrix, position=(next_row,next_col)):
                        moves.append((next_row,next_col))
        return moves
