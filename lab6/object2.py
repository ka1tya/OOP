import random
import tkinter as tk
from tkinter import ttk
from messenger import PORT_OBJECT2
from object_base import Object
from theme import MONO_FONT

class Object2(Object):
    TITLE = "Object2"
    PORT = PORT_OBJECT2

    def build_window(self):
        self.set_state("очікую повідомлення від Lab6")

        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=(0, 10))
        self.text = tk.Text(frame, width=30, height=6, wrap="none", font=(MONO_FONT, 11), state="disabled")
        y_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.text.yview)
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.text.grid(row=0, column=0)
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def on_command(self, command, args):
        if command == "GENERATE":
            n = int(args[0])
            min_value = int(args[1])
            max_value = int(args[2])
            self.generate(n, min_value, max_value)
            return "OK"
        return Object.on_command(self, command, args)

    def generate(self, n, min_value, max_value):
        self.set_state(f"створюю матрицю {n}x{n}...")

        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(random.randint(min_value, max_value))
            matrix.append(row)

        width = max(len(str(min_value)), len(str(max_value))) + 2
        lines = []
        for row in matrix:
            line = ""
            for value in row:
                line += str(value).rjust(width)
            lines.append(line)

        self.text.config(state="normal", width=min(n * width, 60), height=min(n, 15))
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n".join(lines))
        self.text.config(state="disabled")

        buffer_lines = [str(n)]
        for row in matrix:
            words = []
            for value in row:
                words.append(str(value))
            buffer_lines.append(" ".join(words))

        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(buffer_lines))
        self.root.update()  

        self.set_state(f"матрицю {n}x{n} створено і записано в буфер обміну")

if __name__ == "__main__":
    Object2().run()