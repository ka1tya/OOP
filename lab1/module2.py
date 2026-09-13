import tkinter as tk
from tkinter import ttk
 
def show_step1(parent):
    dialog = create_dialog(parent, "Робота2")
    result = [0]
 
    ttk.Label(dialog).pack(padx=20, pady=20)
 
    buttons = ttk.Frame(dialog)
    buttons.pack(pady=(0, 16))
 
    ttk.Button(buttons, text="Далі >", width=10, command=lambda: close_dialog(dialog, result, 1)).pack(side=tk.LEFT, padx=4)
 
    ttk.Button(buttons, text="Відміна", width=10, command=lambda: close_dialog(dialog, result, 0)).pack(side=tk.LEFT, padx=4)
 
    dialog.wait_window()
    return result[0]
 