import unittest
from gameboard import MoveCalculator

class TestMoveCalculator(unittest.TestCase):
    def setUp(self):
        # Set up dummy test data
        self.matrix = [[0,2,1,4,3,2,1,4,0],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,1,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [2,1,4,3,5,1,2,3,4],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,3,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [0,2,3,4,1,2,3,4,0]]
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.center = (self.rows//2, self.cols//2)
        self.move_calculator = MoveCalculator(cant_move=-1)
        self.max_dice_value = 6
    def test_start_at_center_with_no_valid_check(self):
        self.move_calculator.change_cant_move(-100)
        #Dice value cannot be 0 so we don't have to account for 0 value
        for nb_move in range(1,self.max_dice_value + 1):
            valid_moves = self.move_calculator.next_moves(board_matrix=self.matrix, player_pos=self.center, dice_value=nb_move, check_move=False)
            self.assertEqual(len(valid_moves), 4*nb_move)
    def test_start_at_center_valid_check(self):
        #Dice value cannot be 0 so we don't have to account for 0 value
        expect_moves = [4,4,4,4,4,8,8]
        for nb_move in range(1,self.max_dice_value + 1):
            valid_moves = self.move_calculator.next_moves(board_matrix=self.matrix, player_pos=self.center, dice_value=nb_move)
            self.assertEqual(len(valid_moves), expect_moves[nb_move])

if __name__ == '__main__':
    unittest.main()
 