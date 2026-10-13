from shape import Shape
 
class Rectangle(Shape):
    RECT_OUTLINE = "black"
    RECT_FILL = "yellow"
 
    def draw(self, canvas, x1=None, y1=None, x2=None, y2=None):
        if x1 is None:
            x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
 
        color, fill, dash = self._style(self.RECT_OUTLINE, self.RECT_FILL)
        canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=fill, width=2, dash=dash)