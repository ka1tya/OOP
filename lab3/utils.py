import tkinter as tk
 
def add_tooltip(widget, text):
    state = {"window": None}
 
    def show(event):
        if state["window"] is not None:
            return
        win = tk.Toplevel(widget)
        win.overrideredirect(True)  
        win.geometry(f"+{event.x_root + 12}+{event.y_root + 12}")
        label = tk.Label(win, text=text, background="#ffffe0",
                          relief="solid", borderwidth=1, padx=4, pady=2)
        label.pack()
        state["window"] = win
 
    def hide(event):
        if state["window"] is not None:
            state["window"].destroy()
            state["window"] = None
 
    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)
 