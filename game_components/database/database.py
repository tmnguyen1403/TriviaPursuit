from typing import Dict, List, Optional
import requests
from urllib.parse import urljoin

class Database:
    def __init__(self, categories : List[str], questions : Dict[str, List["Question"]]) -> None:
        self.categories = categories
        self.questions = questions
    
    def get_questions(self):
        return self.questions
    
    def get_categories(self):
        return self.categories

async def create_with_online_database(categories = List[str]):
    from question import Question, QuestionType
    import httpx
    database_host = "http://localhost:9000"
    question_category_api = "api/questions/category"
    question_category_url = urljoin(database_host,question_category_api)
    questions = dict()
    result_questions = dict()
    async with httpx.AsyncClient() as client:
        
        #Generate api url
        for category in categories:
            category_name = category.get_name()
            category_api = question_category_url + "/" + category_name
            print("category_api: ", category_api)
            response = await client.get(category_api)
            res_json = response.json()
            questions[category_name] = res_json["questionsByCategory"]
        
        #Save question based on category
        for category, questions in questions.items():
            result_questions[category] = list()
            for question in questions:
                q_obj = Question((question["question"], QuestionType(question["type"]),None, question["answer"], category))
                result_questions[category].append(q_obj)
                
    return Database(categories=categories,questions=result_questions)
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

if __name__ == "__main__":
    categories = ["Math", "Sport", "History", "Movie"]
    create_with_online_database(categories=categories)