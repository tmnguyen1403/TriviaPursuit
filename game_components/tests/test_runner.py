import unittest
from test_question_manager import TestQuestionManager
from test_move_calculator import TestMoveCalculator
if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestQuestionManager))
    test_suite.addTest(unittest.makeSuite(TestMoveCalculator))
    #Add more unit test here when have more files
    unittest.TextTestRunner().run(test_suite)