from abc import ABC, abstractmethod

RUBBER_BAND_COLOR = "blue"
RUBBER_BAND_DASH = (4, 4)  
 
class Shape(ABC):
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._rubber = False  
 
    def set_rubber(self, flag):
        self._rubber = flag
 
    def _style(self, color, fill=""):
        if self._rubber:
            return RUBBER_BAND_COLOR, "", RUBBER_BAND_DASH
        return color, fill, None
 
    @abstractmethod
    def draw(self, canvas):
        raise NotImplementedError