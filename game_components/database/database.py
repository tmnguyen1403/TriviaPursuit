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
    from question import Question
    categories = ["Math", "Science", "Chemistry", "Movie"]
    questions = dict()
    questions["Math"] = []
    questions["Math"].append(Question(("1+1=?","text",None,"2","Math")))
    questions["Math"].append(Question(("2+2=?","text",None,"4","Math")))

    questions["Science"] = []

    questions["Chemistry"] = []
    
    questions["Movie"] = []
    questions["Movie"].append(Question(("OST Titanic?","text",None,"My heart will go on","Movie")))
    questions["Movie"].append(Question(("Director of Avatar 2","text",None,"James Cameron","Movie")))
    return Database(categories,questions)