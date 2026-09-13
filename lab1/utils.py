import tkinter as tk
 
def create_dialog(parent, title):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.resizable(False, False)
    dialog.transient(parent)   
    dialog.grab_set()        
    return dialog
 
def close_dialog(dialog, result_holder, value):
    result_holder[0] = value
    dialog.destroy()
 




