from PySide6.QtWidgets import QLabel, QScrollArea
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class ImageViewer(QScrollArea):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.image_label)
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_pixmap = None

    def display_image(self, image):
        if image is None:
            return
             
        width, height = image.size

        qimage = QImage(image.tobytes(), width, height, width * 3, QImage.Format.Format_RGB888).copy()

        self.original_pixmap = QPixmap.fromImage(qimage)
        self.update_image_size()

    def update_image_size(self):
        if self.original_pixmap is None:
            return

        scaled_pixmap = self.original_pixmap.scaled(
            self.viewport().size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.resize(scaled_pixmap.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image_size()

    def clear(self):
        self.original_pixmap = None
        self.image_label.clear()
        self.image_label.resize(0, 0)