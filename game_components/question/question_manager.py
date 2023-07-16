from typing import Dict, List, Optional
from interface import TileSubscriber
class QuestionManager(TileSubscriber):
    def __init__(self, database: 'Database') -> None:
        self.database = database
        self.current_question = None
        self.curent_category = None
    def update(self, tile: 'Tile', matrix_position) -> bool:
        category = tile.category
        if category not in self.database.categories:
            print(f"question manager does not have category: {category}")
            #Handle special case, this is probably the center tile
            return False
        question = self.get_question(category)
        if question is None:
            print(f"question manager cannot get question of category: {category}")
            return False
        print(f"New question is here: {question.question_text}")
        self.current_question = question
        self.curent_category = category
        print(f"Current category: {self.curent_category}")
    def get_current_question(self) -> 'Question':
        return self.current_question
    def clear_question(self):
        self.current_question = None
    def set_question(self, category: str):
        self.current_question = self.get_question(category=category)
        if self.current_question == None:
            print(f"QuestionManager is out of question from category: {category}")
    def get_question(self, category : str) -> Optional['Question']:
        return_question = None
        if category not in self.database.categories:
            print(f"No category {category} in database")
            return None
        category_questions = self.database.questions[category]
        print(f"questions: {category_questions}")
        if len(category_questions) > 0:
            return_question = category_questions.pop()
            category_questions.append(return_question)
        return return_question