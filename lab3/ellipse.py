from shape import Shape
 
class Ellipse(Shape):
    def draw(self, canvas):
        dx = self._x2 - self._x1
        dy = self._y2 - self._y1
 
        left = self._x1 - dx
        top = self._y1 - dy
        right = self._x1 + dx
        bottom = self._y1 + dy
 
        canvas.create_oval(left, top, right, bottom, outline="black", fill="white", width=2)
 