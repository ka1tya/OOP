from tkinter import ttk

BG = "#f3f4f6"
TEXT = "#1f2937"
MUTED = "#6b7280"
ACCENT = "#2563eb"
ACCENT_DARK = "#1d4ed8"
BORDER = "#d1d5db"
MONO_FONT = "Consolas"
TITLE_FONT = ("Arial", 11, "bold")
RESULT_FONT = ("Arial", 11, "bold") 

def apply_theme(root):
    root.option_add("*Font", "Arial 10")
    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=TEXT)

    style.configure("Muted.TLabel", foreground=MUTED)
    style.configure("Result.TLabel", foreground=ACCENT)

    style.configure("TButton", padding=6)
    style.configure("Accent.TButton", background=ACCENT, foreground="white")
    style.map("Accent.TButton", background=[("active", ACCENT_DARK)])