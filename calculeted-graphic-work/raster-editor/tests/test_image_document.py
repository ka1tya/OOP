import unittest
import tempfile
from pathlib import Path
from PIL import Image
from src.image_document import ImageDocument

class TestImageDocument(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.document = ImageDocument()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_bmp(self):
        path = Path(self.temp_dir.name) / "test.bmp"

        Image.new("RGB", (100, 100), "red").save(path)

        self.document.load(path)

        self.assertTrue(self.document.is_loaded())
        self.assertEqual(self.document.get_image().size, (100, 100))

    def test_save_bmp(self):
        path = Path(self.temp_dir.name) / "result.bmp"

        self.document.image = Image.new("RGB", (50, 50), "blue")
        self.document.save(path)

        self.assertTrue(path.exists())

        with Image.open(path) as image:
            self.assertEqual(image.format, "BMP")
            self.assertEqual(image.mode, "RGB")

    def test_load_invalid_file(self):
        path = Path(self.temp_dir.name) / "invalid.bmp"
        path.write_text("Invalid image")

        with self.assertRaises(ValueError):
            self.document.load(path)

    def test_save_without_image(self):
        path = Path(self.temp_dir.name) / "empty.bmp"

        with self.assertRaises(ValueError):
            self.document.save(path)

if __name__ == "__main__":
    unittest.main()