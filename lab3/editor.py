import tkinter as tk
from tkinter import ttk, messagebox
from point import Point
from line import Line
from rectangle import Rectangle
from ellipse import Ellipse
from icons import point_icon, line_icon, rectangle_icon, ellipse_icon
from utils import add_tooltip
 
RUBBER_BAND_COLOR = "blue"  
 
SHAPE_TYPES = {
    "point": ("Крапка", Point),
    "line": ("Лінія", Line),
    "rectangle": ("Прямокутник", Rectangle),
    "ellipse": ("Еліпс", Ellipse),
}
 
class Editor:
 
    def __init__(self, root):
        self.root = root
        self.root.title("lab3")
        self.root.geometry("800x600")

        self.shapes = []
 
        self.current_type_var = tk.StringVar(value="line")
 
        self.drag_start = None
        self.rubber_band_id = None
        self._icons = {}  
 
        self._build_menu()
        self._build_toolbar()
        self._build_canvas()

    def _build_menu(self):
        menu_bar = tk.Menu(self.root)
 
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
 
        objects_menu = tk.Menu(menu_bar, tearoff=0)
        for key, (name, _) in SHAPE_TYPES.items():
            objects_menu.add_radiobutton(
                label=name,
                variable=self.current_type_var,
                value=key,
            )
        menu_bar.add_cascade(label="Об'єкти", menu=objects_menu)
 
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)
 
        self.root.config(menu=menu_bar)
 
    def _build_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x")
 
        self._icons = {
            "point": point_icon(),
            "line": line_icon(),
            "rectangle": rectangle_icon(),
            "ellipse": ellipse_icon(),
        }
 
        for key, (name, _) in SHAPE_TYPES.items():
            btn = ttk.Radiobutton(
                toolbar,
                image=self._icons[key],
                variable=self.current_type_var,
                value=key,
                style="Toolbutton",
            )
            btn.pack(side="left", padx=2, pady=2)
            add_tooltip(btn, name) 
 
    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)
 
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
 
    def on_button_press(self, event):
        current_type = self.current_type_var.get()
 
        if current_type == "point":
            self.add_shape(Point(event.x, event.y, event.x, event.y))
            self.redraw_all()
            return
 
        self.drag_start = (event.x, event.y)
        self.rubber_band_id = None
 
    def on_mouse_drag(self, event):
        current_type = self.current_type_var.get()
 
        if current_type == "point" or self.drag_start is None:
            return
 
        if self.rubber_band_id is not None:
            self.canvas.delete(self.rubber_band_id)
 
        x1, y1 = self.drag_start
        x2, y2 = event.x, event.y
 
        if current_type == "line":
            self.rubber_band_id = self.canvas.create_line(
                x1, y1, x2, y2, fill=RUBBER_BAND_COLOR
            )
        elif current_type == "rectangle":
            self.rubber_band_id = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=RUBBER_BAND_COLOR
            )
        elif current_type == "ellipse":
            dx, dy = x2 - x1, y2 - y1
            self.rubber_band_id = self.canvas.create_oval(
                x1 - dx, y1 - dy, x1 + dx, y1 + dy, outline=RUBBER_BAND_COLOR
            )
 
    def on_button_release(self, event):
        current_type = self.current_type_var.get()
 
        if current_type == "point" or self.drag_start is None:
            return
 
        if self.rubber_band_id is not None:
            self.canvas.delete(self.rubber_band_id)
            self.rubber_band_id = None
 
        x1, y1 = self.drag_start
        x2, y2 = event.x, event.y
        _, shape_class = SHAPE_TYPES[current_type]
 
        self.add_shape(shape_class(x1, y1, x2, y2))
        self.redraw_all()
 
        self.drag_start = None
 
    def add_shape(self, shape):
        self.shapes.append(shape)  
 
    def redraw_all(self):
        self.canvas.delete("all")
        for shape in self.shapes:
            shape.draw(self.canvas)
 
    def clear_canvas(self):
        self.shapes = []
        self.canvas.delete("all")
 
    def show_about(self):
        messagebox.showinfo(
            "Про програму", "lab3 - інтерфейс користувача. Варіант Ж = 6."
        )