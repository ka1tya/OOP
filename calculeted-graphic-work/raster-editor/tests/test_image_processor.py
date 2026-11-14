import unittest
from PIL import Image
from src.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.image = Image.new("RGB", (10, 10), (100, 80, 60))

    def test_brightness(self):
        result = self.processor.brightness(self.image, 1.5)
        self.assertEqual(result.getpixel((0, 0)), (150, 120, 90))

    def test_contrast(self):
        result = self.processor.contrast(self.image, 0)
        self.assertEqual(result.getpixel((0, 0)), (84, 84, 84))

    def test_rgb(self):
        result = self.processor.rgb(
            self.image, red=2, green=1, blue=1
        )
        self.assertEqual(result.getpixel((0, 0)), (200, 80, 60))

    def test_original_image_is_unchanged(self):
        self.processor.brightness(self.image, 2)
        self.assertEqual(self.image.getpixel((0, 0)), (100, 80, 60))

    def test_invalid_factor(self):
        with self.assertRaises(ValueError):
            self.processor.brightness(self.image, -1)

    def test_missing_image(self):
        with self.assertRaises(ValueError):
            self.processor.brightness(None, 1)

if __name__ == "__main__":
    unittest.main()
