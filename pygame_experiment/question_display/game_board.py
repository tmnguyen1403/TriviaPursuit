from interfaces import CategoryPublisher
from question_manager import QuestionManager
from database import dummy_database, Database
'''
Applying Observer (Publisher Subscriber pattern) to handle category from gameboard

'''

class GameBoard(CategoryPublisher):
    def __init__(self, database: Database):
        self.titles = list(list())
        self.subscribers = list()
        self.category = None
        self.database = database
    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            index = self.subscribers.index(subscriber)
            self.subscribers.pop(index)
    def move(self):
        self.category = "Math"
        self.notify()
    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.category)

if __name__ == "__main__":
    database = dummy_database()
    board = GameBoard(database)
    question_manager = QuestionManager(database=database)
    board.subscribe(question_manager)
    board.move()
    board.move()
    board.move()

