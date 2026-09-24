import tkinter as tk
from tkinter import ttk
 
if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "Arial 10")
 
    style = ttk.Style()
    style.theme_use("clam")
 
    root.mainloop()