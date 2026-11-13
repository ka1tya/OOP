from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QAction
from image_document import ImageDocument
from image_viewer import ImageViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Редактор растрових зображень")
        self.resize(1000, 700)

        self.document = ImageDocument()
        self.viewer = ImageViewer()

        self.setCentralWidget(self.viewer)

        self.create_menu()

    def create_menu(self):
        file_menu = self.menuBar().addMenu("Файл")

        open_action = QAction("Відкрити", self)
        open_action.triggered.connect(self.open_image)

        save_action = QAction("Зберегти як", self)
        save_action.triggered.connect(self.save_image)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Відкрити зображення", "", "BMP Images (*.bmp)")

        if not file_path:
            return

        try:
            self.document.load(file_path)
            self.viewer.display_image(self.document.get_image())
            self.statusBar().showMessage(f"Відкрито: {file_path}")

        except Exception as error:
            QMessageBox.critical(self, "Помилка відкриття", str(error))

    def save_image(self):
        if not self.document.is_loaded():
            QMessageBox.warning(self, "Увага", "Спочатку відкрийте зображення")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Зберегти зображення", "", "BMP Images (*.bmp)")

        if not file_path:
            return

        if not file_path.lower().endswith(".bmp"):
            file_path += ".bmp"

        try:
            self.document.save(file_path)

            QMessageBox.information(self, "Зображення успішно збережено")

        except Exception as error:
            QMessageBox.critical(self, "Помилка збереження", str(error))