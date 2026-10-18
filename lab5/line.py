from shape import Shape
 
class Line(Shape):
    LINE_COLOR = "black"  
 
    def draw(self, canvas, x1=None, y1=None, x2=None, y2=None):
        if x1 is None:
            x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
 
        color, _, dash = self._style(self.LINE_COLOR)
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2, dash=dash)