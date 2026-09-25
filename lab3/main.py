import tkinter as tk
from tkinter import ttk
from editor import Editor
 
if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "Arial 10")
 
    style = ttk.Style()
    style.theme_use("clam")

    editor = Editor(root)
    root.mainloop()