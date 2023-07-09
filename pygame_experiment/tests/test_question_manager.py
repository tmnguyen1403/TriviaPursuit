import unittest

# Use this snippet to import python file in another folder
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
question_folder_path = os.path.join(parrent_dir, 'question_display')
sys.path.append(question_folder_path)

from QuestionManager import QuestionManager

class TestQuestionManager(unittest.TestCase):
    def setUp(self):
        # Set up dummy test data
        self.categories = ["Math", "Science", "Chemistry", "Movie"]
        questions = dict()
        questions["Math"] = ["1+1=","2+2="]
        questions["Science"] = ["cause of thunder","cause of volcano"]
        questions["Chemistry"] = ["product of water reaction","Na + Cl2?"]
        questions["Movie"] = ["Titanic OST","Avatar OST"]
        self.questions = questions
        self.question_manager = QuestionManager(self.categories,self.questions)
    
    def test_get_empty(self):
        question = self.question_manager.get_question("Random")
        self.assertEqual(question, None)
    
    def test_get_first_question(self):
        category = self.categories[0]
        expect_question = self.questions[category][-1]
        question = self.question_manager.get_question(self.categories[0])
        self.assertEqual(question, expect_question)

    def test_get_all_question(self):
        for category in self.categories:
            category_questions = self.questions[category]
            for i in reversed(range(len(category_questions))):
                expect_question = category_questions[i]
                question = self.question_manager.get_question(category)
                self.assertEqual(question, expect_question)
                if i == 0:
                    question = self.question_manager.get_question(category)
                    self.assertEqual(question, None)

if __name__ == '__main__':
    unittest.main()
 