import tkinter as tk
from tkinter import ttk
from utils import create_dialog, close_dialog
 
def show_step2(parent):
    dialog = create_dialog(parent, "Work2")
    result = [0]
 
    ttk.Label(dialog).pack(padx=20, pady=20)
 
    buttons = ttk.Frame(dialog)
    buttons.pack(pady=(0, 16))
 
    ttk.Button(buttons, text="< Назад", width=10, command=lambda: close_dialog(dialog, result, -1)).pack(side="left", padx=4)
 
    ttk.Button(buttons, text="Так", width=10, command=lambda: close_dialog(dialog, result, 1)).pack(side=tk.LEFT, padx=4)
 
    ttk.Button(buttons, text="Відміна", width=10, command=lambda: close_dialog(dialog, result, 0)).pack(side=tk.LEFT, padx=4)
 
    dialog.wait_window()
    return result[0]
 