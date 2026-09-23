from abc import ABC, abstractmethod
 
class Shape(ABC):
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
 
    @abstractmethod
    def draw(self, canvas):
        raise NotImplementedError