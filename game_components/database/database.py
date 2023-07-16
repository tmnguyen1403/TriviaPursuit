from typing import Dict, List, Optional

'''
This singleton pattern is created by chatGPT
'''
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

'''
There can be only one instance of database
'''
@singleton
class Database:
    def __init__(self, categories : List[str], questions : Dict[str, List["Question"]]) -> None:
        self.categories = categories
        self.questions = questions
    
    def get_questions(self):
        return self.questions
    
    def get_categories(self):
        return self.categories

def dummy_database():
    from question import Question, QuestionType
    categories = ["Math", "Science", "Chemistry", "Movie"]
    questions = dict()
    questions["Math"] = []
    questions["Math"].append(Question(("1+1=?",QuestionType.TEXT,None,"2","Math")))
    questions["Math"].append(Question(("2+2=?",QuestionType.TEXT,None,"4","Math")))

    questions["Science"] = []
    questions["Science"].append(Question(("what is science?",QuestionType.TEXT,None,"I don't know","Science")))
    questions["Science"].append(Question(("monte carlo method?",QuestionType.TEXT,None,"I don't know","Science")))
    questions["Chemistry"] = []
    questions["Chemistry"].append(Question(("Name of NaCl?",QuestionType.TEXT,None,"2","Chemistry")))
    questions["Chemistry"].append(Question(("Name of H2O?",QuestionType.TEXT,None,"4","Chemistry")))
    
    questions["Movie"] = []
    questions["Movie"].append(Question(("OST Titanic?",QuestionType.TEXT,None,"My heart will go on","Movie")))
    questions["Movie"].append(Question(("Director of Avatar 2",QuestionType.TEXT,None,"James Cameron","Movie")))
    return Database(categories,questions)