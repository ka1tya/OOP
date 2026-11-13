from PIL import Image
from pathlib import Path
import struct

class ImageDocument:
    def __init__(self):
        self.image = None
        self.file_path = None

    def load(self, file_path):
        file_path = Path(file_path)

        if not file_path.is_file():
            raise FileNotFoundError("Файл не знайдено")

        with open(file_path, "rb") as file:
            header = file.read(30)

        if len(header) < 30 or header[:2] != b"BM":
            raise ValueError("Файл не є коректним BMP-зображенням")

        bits_per_pixel = struct.unpack("<H", header[28:30])[0]

        if bits_per_pixel != 24:
            raise ValueError(
                "Підтримуються тільки BMP-зображення "
                "з глибиною кольору 24 біти"
            )

        with Image.open(file_path) as source:
            if source.format != "BMP":
                raise ValueError("Некоректний формат файлу")

            source.load()
            self.image = source.convert("RGB")

        self.file_path = str(file_path)

    def save(self, file_path):
        if self.image is None:
            raise ValueError("Немає зображення для збереження")

        file_path = Path(file_path)

        if file_path.suffix.lower() != ".bmp":
            file_path = file_path.with_suffix(".bmp")

        self.image.convert("RGB").save(
            file_path,
            format="BMP"
        )

        self.file_path = str(file_path)

    def get_image(self):
        if self.image is None:
            return None

        return self.image.copy()

    def is_loaded(self):
        return self.image is not None