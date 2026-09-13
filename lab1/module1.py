import tkinter as tk
from tkinter import ttk
 
 
def show_work1(parent):
    dialog = create_dialog(parent, "Робота1")
    result = [0]
 
    ttk.Label(dialog).pack(padx=16, pady=(16, 4))
 
    value_var = tk.DoubleVar(value=1)
    value_label = ttk.Label(dialog, text="1")
 
    def on_scale_move(value):
        value_label.config(text=str(int(float(value))))
 
    scale = ttk.Scale(dialog, from_=1, to=100, orient="horizontal", variable=value_var, command=on_scale_move, length=250)
    scale.pack(padx=16)
    value_label.pack(pady=(4, 0))
 
    buttons = ttk.Frame(dialog)
    buttons.pack(pady=16)
 
    ttk.Button(buttons, text="Так", width=10, command=lambda: close_dialog(dialog, result, int(value_var.get()))).pack(side="left", padx=4)
 
    ttk.Button(buttons, text="Відміна", width=10, command=lambda: close_dialog(dialog, result, 0)).pack(side="left", padx=4)
 
    dialog.wait_window() 
    return result[0]