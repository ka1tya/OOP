import tkinter as tk
from tkinter import ttk, messagebox
from point import Point
from line import Line
from rectangle import Rectangle
from ellipse import Ellipse
 
N = 105  
 
shapes = [None] * N
shape_count = 0
 
RUBBER_BAND_COLOR = "red"

SHAPE_TYPES = {
    "point": ("Крапка", Point),
    "line": ("Лінія", Line),
    "rectangle": ("Прямокутник", Rectangle),
    "ellipse": ("Еліпс", Ellipse),
}
 
current_type = "line"    
drag_start = None        
rubber_band_id = None    
 
def set_current_type(type_key):
    global current_type
    current_type = type_key
    update_title()
 
def update_title():
    name, _ = SHAPE_TYPES[current_type]
    root.title(f"lab2 - {name}")
 
def redraw_all():
    canvas.delete("all")
    for shape in shapes[:shape_count]:
        shape.draw(canvas)
 
def add_shape(shape):
    global shape_count
    if shape_count < N:
        shapes[shape_count] = shape
        shape_count += 1
    else:
        messagebox.showwarning("lab2", "Досягнуто максимальної кількості об'єктів")
 
def on_button_press(event):
    global drag_start, rubber_band_id
 
    if current_type == "point":
        add_shape(Point(event.x, event.y, event.x, event.y))
        redraw_all()
        return
 
    drag_start = (event.x, event.y)
    rubber_band_id = None
 
def on_mouse_drag(event):
    global rubber_band_id
 
    if current_type == "point" or drag_start is None:
        return
 
    if rubber_band_id is not None:
        canvas.delete(rubber_band_id)
 
    x1, y1 = drag_start
    x2, y2 = event.x, event.y
 
    if current_type == "line":
        rubber_band_id = canvas.create_line(x1, y1, x2, y2, fill=RUBBER_BAND_COLOR)
 
    elif current_type == "rectangle":
        dx, dy = x2 - x1, y2 - y1
        rubber_band_id = canvas.create_rectangle(
            x1 - dx, y1 - dy, x1 + dx, y1 + dy,
            outline=RUBBER_BAND_COLOR,
        )
 
    elif current_type == "ellipse":
        rubber_band_id = canvas.create_oval(x1, y1, x2, y2, outline=RUBBER_BAND_COLOR)
 
def on_button_release(event):
    global drag_start, rubber_band_id
 
    if current_type == "point" or drag_start is None:
        return
 
    if rubber_band_id is not None:
        canvas.delete(rubber_band_id)
        rubber_band_id = None
 
    x1, y1 = drag_start
    x2, y2 = event.x, event.y
    _, shape_class = SHAPE_TYPES[current_type]
 
    add_shape(shape_class(x1, y1, x2, y2))
    redraw_all()
 
    drag_start = None
 
def clear_canvas():
    global shape_count
    shape_count = 0
    canvas.delete("all")

def show_about():
    messagebox.showinfo("Про програму", "lab2 - розробка графічного редактора об'єктів. Варіант: Ж = 5")
 
root = tk.Tk()
root.geometry("800x600")
 
root.option_add("*Font", "Arial 10")
style = ttk.Style()
style.theme_use("clam")
 
menu_bar = tk.Menu(root)
 
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Очистити", command=clear_canvas)
file_menu.add_separator()
file_menu.add_command(label="Вихід", command=root.quit)
menu_bar.add_cascade(label="Файл", menu=file_menu)
 
objects_menu = tk.Menu(menu_bar, tearoff=0)
for key, (name, _) in SHAPE_TYPES.items():
    objects_menu.add_command(label=name, command=lambda k=key: set_current_type(k))
menu_bar.add_cascade(label="Об'єкти", menu=objects_menu)
 
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Про програму", command=show_about)
menu_bar.add_cascade(label="Довідка", menu=help_menu)
 
root.config(menu=menu_bar)
 
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)
 
canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_button_release)
 
update_title()
 
root.mainloop()