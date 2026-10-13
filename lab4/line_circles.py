from line import Line
from ellipse import Ellipse
 
class LineCircles(Line, Ellipse):
    CIRCLE_RADIUS = 3

    ELLIPSE_OUTLINE = "cyan"
    ELLIPSE_FILL = "cyan"
 
    def draw(self, canvas):
        x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
 
        if self._rubber:
            Line.draw(self, canvas, x1, y1, x2, y2)
            return
 
        r = self.CIRCLE_RADIUS
        step = 4 * r  
 
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        count = max(1, round(length / step))  
 
        for i in range(count + 1):
            t = i / count  
            cx = x1 + (x2 - x1) * t
            cy = y1 + (y2 - y1) * t
            Ellipse.draw(self, canvas, cx, cy, cx + r, cy + r)
 