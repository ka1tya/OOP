from shape import Shape
 
class Line(Shape):
    def draw(self, canvas):
        canvas.create_line(self._x1, self._y1, self._x2, self._y2, fill="black", width=2)
 