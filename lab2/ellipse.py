from shape import Shape
 
class Ellipse(Shape):
    def draw(self, canvas):
        canvas.create_oval(self._x1, self._y1, self._x2, self._y2, outline="black", fill="", width=2)
 