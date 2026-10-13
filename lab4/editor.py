import tkinter as tk
from tkinter import ttk, messagebox
from point import Point
from line import Line
from rectangle import Rectangle
from ellipse import Ellipse
from line_circles import LineCircles
from cube import Cube
from icons import (point_icon, line_icon, rectangle_icon, ellipse_icon, line_circles_icon, cube_icon)
from utils import add_tooltip
 
SHAPE_TYPES = {
    "point": ("Крапка", Point, point_icon),
    "line": ("Лінія", Line, line_icon),
    "rectangle": ("Прямокутник", Rectangle, rectangle_icon),
    "ellipse": ("Еліпс", Ellipse, ellipse_icon),
    "line_circles": ("Лінія з кружечками", LineCircles, line_circles_icon),
    "cube": ("Каркас куба", Cube, cube_icon),
}
 
class MyEditor:
 
    def __init__(self, root):
        self.root = root
        self.root.title("lab4")
        self.root.geometry("800x600")

        self.shapes = []
 
        self.current_type_var = tk.StringVar(value="line")
 
        self.drag_start = None
        self.icons = {}  
 
        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
 
    # Побудова інтерфейсу 
    def _build_menu(self):
        menu_bar = tk.Menu(self.root)
 
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
 
        objects_menu = tk.Menu(menu_bar, tearoff=0)
        for key, (name, _, _) in SHAPE_TYPES.items():
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
 
        for key, (name, _, make_icon) in SHAPE_TYPES.items():
            self.icons[key] = make_icon()
            btn = ttk.Radiobutton(
                toolbar,
                image=self.icons[key],
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
 
    # Обробники миші (однакові для будь-якої фігури)
    def on_button_press(self, event):
        self.drag_start = (event.x, event.y)
 
    def on_mouse_drag(self, event):
        if self.drag_start is None:
            return
 
        rubber = self.make_shape(event.x, event.y)
        rubber.set_rubber(True)       
        self.redraw_all()             
        rubber.draw(self.canvas)      
 
    def on_button_release(self, event):
        if self.drag_start is None:
            return
 
        self.add_shape(self.make_shape(event.x, event.y))
        self.drag_start = None
        self.redraw_all()
 
    # Робота з фігурами
    def make_shape(self, x2, y2):
        x1, y1 = self.drag_start
        _, shape_class, _ = SHAPE_TYPES[self.current_type_var.get()]
        return shape_class(x1, y1, x2, y2)
 
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
        messagebox.showinfo("Про програму", "lab4 - графічний редактор об'єктів")
 