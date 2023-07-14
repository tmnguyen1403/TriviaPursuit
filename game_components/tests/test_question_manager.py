import unittest

# Use this snippet to import python file in another folder
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
question_folder_path = os.path.join(parrent_dir, 'question_display')
sys.path.append(question_folder_path)

from question_manager import QuestionManager
from database import dummy_database
import copy
class TestQuestionManager(unittest.TestCase):
    def setUp(self):
        # Set up dummy test data
        data = dummy_database()
        self.data = data
        self.question_manager = QuestionManager(data)
        self.categories = data.get_categories()
        self.questions = data.get_questions()
    def test_get_empty(self):
        question = self.question_manager.get_question("Random")
        self.assertEqual(question, None)
    
    def test_get_first_question(self):
        #Deep copy questions due to data is a singleton, modifying questions will reflect to the next test
        questions = copy.deepcopy(self.questions)
        category = self.categories[0]
        expect_question = self.questions[category][-1]
        question = self.question_manager.get_question(self.categories[0])
        self.assertEqual(question, expect_question)
        self.data.questions = questions

    def test_get_all_question(self):
        #Deep copy questions due to data is a singleton, modifying questions will reflect to the next test
        questions = copy.deepcopy(self.questions)
        for category in self.categories:
            category_questions = self.questions[category]
            for i in reversed(range(len(category_questions))):
                expect_question = category_questions[i]
                question = self.question_manager.get_question(category)
                self.assertEqual(question, expect_question)
                if i == 0:
                    question = self.question_manager.get_question(category)
                    self.assertEqual(question, None)
        self.data.questions = questions

if __name__ == '__main__':
    unittest.main()
 