import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from point import Point
from line import Line
from rectangle import Rectangle
from ellipse import Ellipse
from line_circles import LineCircles
from cube import Cube
from icons import (point_icon, line_icon, rectangle_icon, ellipse_icon, line_circles_icon, cube_icon)
from utils import add_tooltip
from table import MyTable
from file import save_rows, load_rows
 
SHAPE_TYPES = {
    "point": ("Крапка", Point, point_icon),
    "line": ("Лінія", Line, line_icon),
    "rectangle": ("Прямокутник", Rectangle, rectangle_icon),
    "ellipse": ("Еліпс", Ellipse, ellipse_icon),
    "line_circles": ("Лінія з кружечками", LineCircles, line_circles_icon),
    "cube": ("Каркас куба", Cube, cube_icon),
}
 
class MyEditor:
    _allow_create = False
 
    @staticmethod
    def instance(root=None):
        if not hasattr(MyEditor.instance, "obj"):
            if root is None:
                raise RuntimeError("Перший виклик instance() потребує вікно root")
            MyEditor._allow_create = True
            MyEditor.instance.obj = MyEditor(root)
            MyEditor._allow_create = False
        return MyEditor.instance.obj
 
    def __init__(self, root):
        if not MyEditor._allow_create:
            raise RuntimeError("MyEditor - Singleton: використовуйте MyEditor.instance()")
 
        self.root = root
        self.root.title("lab5")
        self.root.geometry("800x600")

        self.shapes = []
        self.selected_index = None  

        self.table = None
        self.table_var = tk.BooleanVar(value=False)  

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
        file_menu.add_command(label="Зберегти", command=self.save_to_file)
        file_menu.add_command(label="Відкрити", command=self.load_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.destroy)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
 
        objects_menu = tk.Menu(menu_bar, tearoff=0)
        for key, (name, _, _) in SHAPE_TYPES.items():
            objects_menu.add_radiobutton(
                label=name,
                variable=self.current_type_var,
                value=key,
            )
        menu_bar.add_cascade(label="Об'єкти", menu=objects_menu)
 
        window_menu = tk.Menu(menu_bar, tearoff=0)
        window_menu.add_checkbutton(
            label="Таблиця об'єктів",
            variable=self.table_var,
            command=self.on_toggle_table,
        )
        menu_bar.add_cascade(label="Вікно", menu=window_menu)
 
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
 
    # Обробники миші 
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
 
    def key_of(self, shape):
        for key, (_, shape_class, _) in SHAPE_TYPES.items():
            if type(shape) is shape_class:
                return key
 
    def add_shape(self, shape):
        self.shapes.append(shape)
        self.selected_index = None
        self.update_table()
 
    def redraw_all(self):
        self.canvas.delete("all")
        for index, shape in enumerate(self.shapes):
            shape.set_selected(index == self.selected_index)
            shape.draw(self.canvas)
 
    def clear_canvas(self):
        self.shapes = []
        self.selected_index = None
        self.canvas.delete("all")
        self.update_table()
 
    # Вікно таблиці 
    def on_toggle_table(self):
        if self.table_var.get():
            self.table = MyTable(
                self.root,
                on_select=self.on_table_select,
                on_delete=self.on_table_delete,
                on_close=self.on_table_closed,
            )
            self.update_table()
        elif self.table is not None:
            self.table.close()
            self.on_table_closed()
 
    def update_table(self):
        if self.table is None:
            return
        rows = []
        for shape in self.shapes:
            name = SHAPE_TYPES[self.key_of(shape)][0]
            x1, y1, x2, y2 = shape.coords()
            rows.append((name, x1, y1, x2, y2))
        self.table.set_rows(rows)
 
    # Callback-функції (їх викликає таблиця, коли щось сталося)
    def on_table_select(self, index):
        self.selected_index = index
        self.redraw_all()
 
    def on_table_delete(self, index):
        del self.shapes[index]
        self.selected_index = None
        self.redraw_all()
        self.update_table()
 
    def on_table_closed(self):
        self.table = None
        self.table_var.set(False)  
        self.selected_index = None
        self.redraw_all()
 
    # Файл
    def save_to_file(self):
        path = filedialog.asksaveasfilename(
            title="Зберегти об'єкти",
            defaultextension=".csv",
            filetypes=[("CSV файли", "*.csv")],
        )
        if not path:
            return
 
        rows = []
        for shape in self.shapes:
            x1, y1, x2, y2 = shape.coords()
            rows.append((self.key_of(shape), x1, y1, x2, y2))
 
        try:
            save_rows(path, rows)
        except OSError as error:
            messagebox.showerror("lab5", f"Не вдалося зберегти файл:\n{error}")
 
    def load_from_file(self):
        path = filedialog.askopenfilename(
            title="Відкрити об'єкти",
            filetypes=[("CSV файли", "*.csv")],
        )
        if not path:
            return
 
        try:
            new_shapes = []
            for key, x1, y1, x2, y2 in load_rows(path):
                shape_class = SHAPE_TYPES[key][1]
                new_shapes.append(shape_class(x1, y1, x2, y2))
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror("lab5", f"Не вдалося відкрити файл:\n{error}")
            return
 
        # Завантажені фігури замінюють поточні
        self.shapes = new_shapes
        self.selected_index = None
        self.redraw_all()
        self.update_table()
 
    def show_about(self):
        messagebox.showinfo("Про програму", "lab5 - багатовіконний графічний редактор")