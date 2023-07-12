from typing import Dict, List, Optional
from question import Question
from interfaces import CategorySubscriber
from database import Database
class QuestionManager(CategorySubscriber):
    def __init__(self, database: Database) -> None:
        self.database = database
        self.current_question = None
    def update(self, category) -> bool:
        if category not in self.database.categories:
            print(f"question manager does not have category: {category}")
            return False
        question = self.get_question(category)
        if question is None:
            print(f"question manager cannot get question of category: {category}")
            return False
        print(f"New question is here: {question.question_text}")
        self.current_question = question
    def get_current_question(self) -> Question:
        return self.current_question
    def clear_question(self):
        self.current_question = None

    def get_question(self, category : str) -> Optional[Question]:
        if category not in self.database.categories:
            return None
        category_questions = self.database.questions[category]
        if len(category_questions) > 0:
            return category_questions.pop()
        return None