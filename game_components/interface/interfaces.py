from abc import ABC, abstractmethod

class CategorySubscriber(ABC):
    @abstractmethod
    def update(self,category) -> bool:
        pass

class CategoryPublisher(ABC): 
    @abstractmethod
    def subscribe(self,subscriber):
        pass
    @abstractmethod
    def unsubscribe(self,subscriber):
        pass
    @abstractmethod
    def notify(self):
        pass