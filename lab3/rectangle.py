from shape import Shape
 
class Rectangle(Shape):
    def draw(self, canvas):
        canvas.create_oval(self._x1, self._y1, self._x2, self._y2, outline="black", fill="yellow", width=2)
 