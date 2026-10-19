import tkinter as tk
from tkinter import ttk
 
from editor import MyEditor
 
root = tk.Tk()
root.option_add("*Font", "Arial 10")
 
style = ttk.Style()
style.theme_use("clam")
 
editor = MyEditor.singleton(root)
 
root.mainloop()