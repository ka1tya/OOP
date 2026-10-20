def save_rows(path, rows):
    with open(path, "w", encoding="utf-8") as file:
        for key, x1, y1, x2, y2 in rows:
            file.write(f"{key},{x1},{y1},{x2},{y2}\n")
 
def load_rows(path):
    rows = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            key, x1, y1, x2, y2 = line.split(",")
            rows.append((key, int(x1), int(y1), int(x2), int(y2)))
    return rows