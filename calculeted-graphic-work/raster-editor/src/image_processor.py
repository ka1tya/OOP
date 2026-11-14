from PIL import Image, ImageEnhance

class ImageProcessor:
    def brightness(self, image, factor):
        self._validate_image(image)
        self._validate_factor(factor)

        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    def contrast(self, image, factor):
        self._validate_image(image)
        self._validate_factor(factor)

        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    def rgb(self, image, red=1.0, green=1.0, blue=1.0):
        self._validate_image(image)

        for factor in (red, green, blue):
            self._validate_factor(factor)

        image = image.convert("RGB")

        r, g, b = image.split()

        r = r.point(lambda value: min(255, int(value * red)))
        g = g.point(lambda value: min(255, int(value * green)))
        b = b.point(lambda value: min(255, int(value * blue)))

        return Image.merge("RGB", (r, g, b))

    @staticmethod
    def _validate_image(image):
        if image is None:
            raise ValueError("Зображення не завантажено")

    @staticmethod
    def _validate_factor(factor):
        if not isinstance(factor, (int, float)) or factor < 0:
            raise ValueError("Коефіцієнт повинен бути невід'ємним числом")
