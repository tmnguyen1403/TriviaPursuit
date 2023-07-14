import unittest
from test_question_manager import TestQuestionManager

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestQuestionManager))
    #Add more unit test here when have more files
    unittest.TextTestRunner().run(test_suite)