from enum import Enum

class QuestionType(Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
class Question:
    def __init__(self, data):
        question_text, mime_type, link, answer, category = data
        self.question_text = question_text
        self.mime_type = QuestionType(mime_type) #text, audio, video question
        self.link = link # Use for audio/video question
        self.answer = answer # Store correct answer
        self.category = category #
    def get_text(self):
        return self.question_text
    #Category can be a class as well to have its own icon for example
    def get_category(self):
        return self.category
    #Answer can be a class as well since it can have its own type 
    def get_answer(self):
        return self.answer
    