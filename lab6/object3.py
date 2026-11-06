import tkinter as tk
from tkinter import ttk
from fractions import Fraction
from messenger import PORT_OBJECT3
from object_base import Object
from theme import RESULT_FONT

def parse_matrix(text):
    lines = text.strip().splitlines()
    if not lines:
        raise ValueError("порожній текст")

    n = int(lines[0])
    matrix = []
    for line in lines[1:n + 1]:
        row = []
        for word in line.split():
            row.append(int(word))
        if len(row) != n:
            raise ValueError("неправильна довжина рядка")
        matrix.append(row)
    if len(matrix) != n:
        raise ValueError("рядків менше, ніж n")
    return matrix

def determinant(matrix):
    n = len(matrix)
    a = []
    for row in matrix:
        new_row = []
        for value in row:
            new_row.append(Fraction(value))
        a.append(new_row)

    result = Fraction(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return 0

        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result

        result *= a[col][col]

        for row in range(col + 1, n):
            factor = a[row][col] / a[col][col]
            for k in range(col, n):
                a[row][k] -= factor * a[col][k]

    return int(result)

class Object3(Object):
    TITLE = "Object3"
    PORT = PORT_OBJECT3

    def build_window(self):
        self.set_state("очікую повідомлення від Lab6")

        self.info_var = tk.StringVar(value="Матриці ще немає")
        self.result_var = tk.StringVar(value="-")
        ttk.Label(self.root, textvariable=self.info_var, style="Muted.TLabel").pack(padx=20, pady=(10, 0))
        ttk.Label(self.root, textvariable=self.result_var, style="Result.TLabel", font=RESULT_FONT).pack(padx=20, pady=(6, 16))

    def on_command(self, command, args):
        if command == "SHOW":
            return self.show_determinant()
        return Object.on_command(self, command, args)

    def show_determinant(self):
        self.set_state("читаю матрицю з буфера обміну...")

        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            self.set_state("буфер обміну порожній")
            return "ERROR буфер обміну порожній"

        try:
            matrix = parse_matrix(text)
        except ValueError:
            self.set_state("в буфері обміну немає матриці")
            return "ERROR в буфері обміну немає матриці"

        value = determinant(matrix)
        n = len(matrix)
        self.info_var.set(f"Матриця {n}x{n} (з буфера обміну)")
        self.result_var.set(f"Визначник = {value}")
        self.set_state("визначник обчислено")
        return f"OK {value}"

if __name__ == "__main__":
    Object3().run()