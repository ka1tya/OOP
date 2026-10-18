from line import Line
from rectangle import Rectangle
 
class Cube(Line, Rectangle):
    LINE_COLOR = "pink"
    RECT_OUTLINE = "pink"
    RECT_FILL = ""
 
    def draw(self, canvas):
        x1, y1 = self._x1, self._y1
 
        side = max(abs(self._x2 - x1), abs(self._y2 - y1))
        if self._x2 >= x1:
            x2 = x1 + side
        else:
            x2 = x1 - side
        if self._y2 >= y1:
            y2 = y1 + side
        else:
            y2 = y1 - side
 
        d = side // 2  

        Rectangle.draw(self, canvas, x1 + d, y1 - d, x2 + d, y2 - d)
        Rectangle.draw(self, canvas, x1, y1, x2, y2)                  

        Line.draw(self, canvas, x1, y1, x1 + d, y1 - d)
        Line.draw(self, canvas, x2, y1, x2 + d, y1 - d)
        Line.draw(self, canvas, x1, y2, x1 + d, y2 - d)
        Line.draw(self, canvas, x2, y2, x2 + d, y2 - d)