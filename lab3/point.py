from shape import Shape
 
POINT_RADIUS = 3
 
class Point(Shape):
    def draw(self, canvas):
        x, y = self._x1, self._y1
        canvas.create_oval(
            x - POINT_RADIUS, y - POINT_RADIUS,
            x + POINT_RADIUS, y + POINT_RADIUS,
            fill="black", outline="black",
        )
 