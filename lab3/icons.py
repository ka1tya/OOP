import math
import tkinter as tk
 
ICON_SIZE = 20
FG = "#000000"
BG = "#ffffff"
 
def _new_icon():
    icon = tk.PhotoImage(width=ICON_SIZE, height=ICON_SIZE)
    icon.put(BG, to=(0, 0, ICON_SIZE, ICON_SIZE))
    return icon
 
def point_icon():
    icon = _new_icon()
    c = ICON_SIZE // 2
    r = 3
    icon.put(FG, to=(c - r, c - r, c + r, c + r))
    return icon
 
def line_icon():
    icon = _new_icon()
    for i in range(ICON_SIZE):
        icon.put(FG, (i, i))
    return icon
 
def rectangle_icon():
    icon = _new_icon()
    m = 3  
    for x in range(m, ICON_SIZE - m):
        icon.put(FG, (x, m))
        icon.put(FG, (x, ICON_SIZE - m - 1))
    for y in range(m, ICON_SIZE - m):
        icon.put(FG, (m, y))
        icon.put(FG, (ICON_SIZE - m - 1, y))
    return icon
 
def ellipse_icon():
    icon = _new_icon()
    cx = cy = ICON_SIZE / 2
    rx = ICON_SIZE / 2 - 3
    ry = ICON_SIZE / 2 - 5
    for deg in range(0, 360, 2):
        rad = math.radians(deg)
        x = int(cx + rx * math.cos(rad))
        y = int(cy + ry * math.sin(rad))
        if 0 <= x < ICON_SIZE and 0 <= y < ICON_SIZE:
            icon.put(FG, (x, y))
    return icon
 