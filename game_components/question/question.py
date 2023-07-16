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