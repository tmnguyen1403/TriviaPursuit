from abc import ABC, abstractmethod

class TileSubscriber(ABC):
    @abstractmethod
    def update(self,tile,matrix_position) -> bool:
        pass

class TilePublisher(ABC): 
    @abstractmethod
    def subscribe(self,subscriber):
        pass
    @abstractmethod
    def unsubscribe(self,subscriber):
        pass
    @abstractmethod
    def notify(self):
        pass