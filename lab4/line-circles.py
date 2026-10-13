from line import Line
from ellipse import Ellipse
 
class LineCircles(Line, Ellipse):
    CIRCLE_RADIUS = 6
 
    LINE_COLOR = "red"
    ELLIPSE_OUTLINE = "red"
    ELLIPSE_FILL = "white"
 
    def draw(self, canvas):
        x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
        r = self.CIRCLE_RADIUS
 
        Line.draw(self, canvas, x1, y1, x2, y2)             
        Ellipse.draw(self, canvas, x1, y1, x1 + r, y1 + r)  
        Ellipse.draw(self, canvas, x2, y2, x2 + r, y2 + r)  