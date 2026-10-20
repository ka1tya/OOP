import tkinter as tk
from tkinter import ttk
 
class MyTable:
    COLUMN_IDS = ("object", "x1", "y1", "x2", "y2")
    COLUMN_TITLES = ("Об'єкт", "x1", "y1", "x2", "y2")
 
    def __init__(self, parent, on_select=None, on_delete=None, on_close=None):
        self.on_select = on_select 
        self.on_delete = on_delete  
        self.on_close = on_close   
 
        self._selected = None 
 
        self.window = tk.Toplevel(parent)
        self.window.title("Таблиця об'єктів")
        self.window.transient(parent)  
        
        x = parent.winfo_rootx() + parent.winfo_width() + 10
        if x + 440 > parent.winfo_screenwidth():
            x = parent.winfo_rootx() + 60
        y = parent.winfo_rooty()
        self.window.geometry(f"440x300+{x}+{y}")
 
        self.window.protocol("WM_DELETE_WINDOW", self._handle_close)
 
        frame = ttk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=6, pady=6)
 
        self.tree = ttk.Treeview(frame, columns=self.COLUMN_IDS, show="headings", selectmode="browse")
        for column_id, title in zip(self.COLUMN_IDS, self.COLUMN_TITLES):
            self.tree.heading(column_id, text=title)
            self.tree.column(column_id, width=60, anchor="center")
        self.tree.column("object", width=170, anchor="w")
 
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
 
        ttk.Button(self.window, text="Видалити виділений", command=self._handle_delete).pack(pady=(0, 8))
 
        self.tree.bind("<<TreeviewSelect>>", self._handle_select)
        self.tree.bind("<Delete>", lambda event: self._handle_delete())

    # Інтерфейс для зовнішнього коду
    def set_rows(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
        self._selected = None
 
    def close(self):
        self.window.destroy()
 
    # Внутрішні обробники подій
    def _handle_select(self, event):
        selection = self.tree.selection()
        if selection:
            index = self.tree.index(selection[0])
        else:
            index = None
 
        if index == self._selected:
            return
        self._selected = index
        if self.on_select is not None:
            self.on_select(index)
 
    def _handle_delete(self):
        if self._selected is not None and self.on_delete is not None:
            self.on_delete(self._selected)
 
    def _handle_close(self):
        self.window.destroy()
        if self.on_close is not None:
            self.on_close()