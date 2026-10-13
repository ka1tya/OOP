from shape import Shape
 
class Ellipse(Shape):
    ELLIPSE_OUTLINE = "black"
    ELLIPSE_FILL = "white"
 
    def draw(self, canvas, x1=None, y1=None, x2=None, y2=None):
        if x1 is None:
            x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
 
        dx = x2 - x1
        dy = y2 - y1
 
        color, fill, dash = self._style(self.ELLIPSE_OUTLINE, self.ELLIPSE_FILL)
        canvas.create_oval(x1 - dx, y1 - dy, x1 + dx, y1 + dy, outline=color, fill=fill, width=2, dash=dash)