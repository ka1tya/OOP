import tkinter as tk
from tkinter import ttk
from editor import MyEditor
from table import MyTable

root = tk.Tk()
root.option_add("*Font", "Arial 10")

style = ttk.Style()
style.theme_use("clam")

editor = MyEditor.singleton(root)

table = MyTable(
    root,
    on_select=editor.on_table_select,
    on_delete=editor.on_table_delete,
    on_close=editor.on_table_closed,
)
editor.set_table(table)

root.mainloop()