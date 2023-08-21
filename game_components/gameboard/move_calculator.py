from typing import Dict, List, Optional, Tuple

class MoveCalculator:
    def __init__(self, cant_move):
        self.cant_move = cant_move
        self.directions = [(0,-1),(0,1),(-1,0),(1,0)]

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
    
    def move_helper(self, current_pos, board_matrix: List[List[int]], moved_matrix, remaining_move, moves):
        if remaining_move == 0:
            moves.append(current_pos)
            return

        #Actual move search
        current_x, current_y = current_pos
        for direction in self.directions:
            x,y = direction
            #Calculate next move
            nx,ny = (current_x + x, current_y + y)
            next_move = (nx,ny)
            if self.is_movable(board_matrix, next_move) and moved_matrix[nx][ny] == 0:
                moved_matrix[nx][ny] = 1
                self.move_helper(next_move, board_matrix, moved_matrix, remaining_move - 1, moves)
                moved_matrix[nx][ny] = 0

    def next_moves(self, board_matrix: List[List[int]], player_pos:Tuple[int,int], dice_value: int):
        moves = []
        px, py = player_pos
        print(f"player pos: {px},{py}")
        nb_row = len(board_matrix)
        nb_col = len(board_matrix[0])
        moved_matrix = [[0 for _ in range(nb_row)] for _ in range(nb_col)]
        print(moved_matrix)
        # Mark the current position is taken on moved matrix
        moved_matrix[px][py] = 1
        self.move_helper(current_pos=player_pos, board_matrix=board_matrix, moved_matrix=moved_matrix, remaining_move=dice_value, moves=moves)

        print("******All possible moves******")
        print(moves)
        print("******END All possible moves END******")

        return moves