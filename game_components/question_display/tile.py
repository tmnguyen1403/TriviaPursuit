from interfaces import CategoryPublisher
from question_manager import QuestionManager
from database import dummy_database, Database

class Tile:
    def __init__(self, category, color, rect, type):
        self.category = category
        self.color = color
        self.rect = rect #(x,y,width,height)
        self.type = type #Allows to perform certain action depending on tile
