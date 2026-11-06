import tkinter as tk
from tkinter import ttk
from messenger import open_server, handle_one_request
from theme import apply_theme

class Object:
    TITLE = "Object"  
    PORT = 0          

    def __init__(self):
        self.server = open_server(self.PORT)
        if self.server is None:
            raise SystemExit(f"{self.TITLE} вже запущено")

        self.root = tk.Tk()
        self.root.title(self.TITLE)
        apply_theme(self.root)
        self.state_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.state_var).pack(anchor="w", padx=10, pady=(10, 4))

        self.build_window()  

        self.root.after(100, self._poll)

    def build_window(self):
        pass

    def on_command(self, command, args):
        return "ERROR невідома команда " + command

    def set_state(self, text):
        self.state_var.set("Стан: " + text)
        self.root.update_idletasks()

    def run(self):
        self.root.mainloop()

    def _poll(self):
        try:
            handle_one_request(self.server, self.handle_message)
        except OSError:
            pass 
        self.root.after(100, self._poll)

    def handle_message(self, text):
        try:
            return self._dispatch(text)
        except Exception as error:
            return f"ERROR {error}"

    def _dispatch(self, text):
        parts = text.split()
        if not parts:
            return "ERROR порожнє повідомлення"
        command, args = parts[0], parts[1:]

        if command == "PING":
            return "OK"

        if command == "PLACE":
            x, y = int(args[0]), int(args[1])
            self.root.geometry(f"+{x}+{y}")
            self.root.update_idletasks() 
            self.root.lift()
            return "OK"

        if command == "QUIT":
            self.root.after(200, self.root.destroy)
            return "OK"

        return self.on_command(command, args)