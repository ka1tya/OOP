import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
from messenger import send_message, PORT_OBJECT2, PORT_OBJECT3
from theme import apply_theme, MONO_FONT, TITLE_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WINDOW_W = 420
WINDOW_H = 330
MAX_N = 15

def parse_parameters(n_text, min_text, max_text):
    try:
        n = int(n_text)
        min_value = int(min_text)
        max_value = int(max_text)
    except ValueError:
        raise ValueError("n, Min і Max мають бути цілими числами")

    if n < 1 or n > MAX_N:
        raise ValueError(f"n має бути від 1 до {MAX_N}.")
    if min_value > max_value:
        raise ValueError("Min не може бути більшим за Max")
    return n, min_value, max_value

class Lab6:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab6")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}+20+20")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.busy = False  # True, поки йде виконання (щоб не запустити удруге)
        self.last_determinant = None
        self.session_number = 0

        self._build_menu()
        self._build_window()
        self.set_state("очікую вибору пункту меню")

    # Вікно та меню 
    def _build_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Вихід", command=self.on_exit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        work_menu = tk.Menu(menu_bar, tearoff=0)
        work_menu.add_command(label="Виконати", command=self.on_run)
        menu_bar.add_cascade(label="Робота", menu=work_menu)

        self.root.config(menu=menu_bar)

    def _build_window(self):
        self.state_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.state_var, font=TITLE_FONT).pack(anchor="w", padx=10, pady=(10, 4))

        # Журнал
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_text = tk.Text(frame, height=10, wrap="word", font=(MONO_FONT, 9), state="disabled")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def set_state(self, text):
        self.state_var.set("Стан: " + text)
        self.root.update()

    def log(self, text):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()

    # Діалог параметрів 
    def ask_parameters(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Параметри матриці")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.wait_visibility()
        dialog.grab_set()

        n_var = tk.StringVar(value="4")
        min_var = tk.StringVar(value="-9")
        max_var = tk.StringVar(value="9")

        fields = (("n (розмір матриці):", n_var), ("Min:", min_var), ("Max:", max_var))
        for row, (label_text, var) in enumerate(fields):
            ttk.Label(dialog, text=label_text).grid(row=row, column=0, sticky="w", padx=12, pady=6)
            ttk.Entry(dialog, textvariable=var, width=12).grid(row=row, column=1, sticky="w", padx=12, pady=6)

        result = [None]

        def on_ok():
            try:
                result[0] = parse_parameters(n_var.get(), min_var.get(), max_var.get())
            except ValueError as error:
                messagebox.showerror("Помилка", str(error), parent=dialog)
                return
            dialog.destroy()

        buttons = ttk.Frame(dialog)
        buttons.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(buttons, text="Виконати", width=10, command=on_ok).pack(side="left", padx=4)
        ttk.Button(buttons, text="Відміна", width=10, command=dialog.destroy).pack(side="left", padx=4)
        dialog.bind("<Return>", lambda event: on_ok())

        dialog.wait_window()
        return result[0]

    # Головна робота
    def on_run(self):
        if self.busy:
            return
        params = self.ask_parameters()
        if params is None:
            return
        n, min_value, max_value = params

        self.busy = True
        try:
            self.run_session(n, min_value, max_value)
        finally:
            self.busy = False

    def ensure_running(self, name, port, script):
        if send_message(port, "PING", timeout=0.5) is not None:
            self.log(f"{name} вже запущено - користуюсь нею")
            return True

        self.log(f"{name} не знайдено - запускаю")
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, script)])

        for attempt in range(60):
            time.sleep(0.1)
            self.root.update()
            if send_message(port, "PING", timeout=0.5) is not None:
                self.log(f"{name} запущено")
                return True

        self.log(f"Не вдалося запустити {name}")
        return False

    def run_session(self, n, min_value, max_value):
        self.session_number += 1
        if self.session_number > 1:
            self.log("")
        self.log(f"Сеанс {self.session_number}: n={n}, Min={min_value}, Max={max_value}")
        self.last_determinant = None

        # Object2 створює матрицю
        self.set_state("шукаю Object2")
        if not self.ensure_running("Object2", PORT_OBJECT2, "object2.py"):
            self.set_state("помилка")
            return

        self.set_state("Object2 створює матрицю")
        command = f"GENERATE {n} {min_value} {max_value}"
        self.log(f"Lab6 -> Object2: {command}")
        reply = send_message(PORT_OBJECT2, command, timeout=10)
        self.log(f"Object2 -> Lab6: {reply}")
        if reply != "OK":
            self.set_state("помилка")
            return

        # Object3 рахує визначник
        self.set_state("шукаю Object3")
        if not self.ensure_running("Object3", PORT_OBJECT3, "object3.py"):
            self.set_state("помилка")
            return

        self.set_state("Object3 рахує визначник")
        self.log("Lab6 -> Object3: SHOW")
        reply = send_message(PORT_OBJECT3, "SHOW", timeout=10)
        self.log(f"Object3 -> Lab6: {reply}")
        if reply is None or not reply.startswith("OK"):
            self.set_state("помилка")
            return
        self.last_determinant = int(reply[3:])

        self.set_state("розставляю вікна")
        self.arrange_windows()

        self.set_state(f"готово, визначник = {self.last_determinant}")

    def arrange_windows(self):
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}+20+20")
        self.log("Lab6 -> Object2: PLACE (розставити вікна)")
        send_message(PORT_OBJECT2, f"PLACE {20 + WINDOW_W + 20} 20")
        self.log("Lab6 -> Object3: PLACE (розставити вікна)")
        send_message(PORT_OBJECT3, f"PLACE 20 {20 + WINDOW_H + 100}")
        self.root.lift()

    def on_exit(self):
        send_message(PORT_OBJECT2, "QUIT", timeout=1.0)
        send_message(PORT_OBJECT3, "QUIT", timeout=1.0)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    apply_theme(root)

    Lab6(root)
    root.mainloop()