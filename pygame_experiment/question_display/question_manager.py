from typing import Dict, List, Optional
from question import Question
class QuestionManager:
    def __init__(self, categories : List[str], questions : Dict[str, List[Question]]) -> None:
        self.categories = categories
        self.questions = questions
    def get_question(self, category : str) -> Optional[Question]:
        if category not in self.categories:
            return None
        category_questions = self.questions[category]
        if len(category_questions) > 0:
            return category_questions.pop()
        return None