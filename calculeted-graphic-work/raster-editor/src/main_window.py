from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from image_document import ImageDocument
from image_viewer import ImageViewer
from toolbar import MainToolBar, EditMode

MODE_NAMES = {
    EditMode.BRIGHTNESS: "Світлота",
    EditMode.CONTRAST: "Контраст",
    EditMode.RGB: "Корекція RGB",
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Редактор растрових зображень")
        self.resize(1000, 700)

        self.document = ImageDocument()
        self.viewer = ImageViewer()

        self.setCentralWidget(self.viewer)

        self.create_toolbar()
        self.create_menu()

        self.statusBar().showMessage("Готово")

    def create_toolbar(self):
        self.toolbar = MainToolBar(self)
        self.addToolBar(self.toolbar)

        self.toolbar.open_requested.connect(self.open_image)
        self.toolbar.save_requested.connect(self.save_image)
        self.toolbar.save_as_requested.connect(self.save_image_as)
        self.toolbar.mode_changed.connect(self.on_mode_changed)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("Файл")

        file_menu.addAction(self.toolbar.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.toolbar.save_action)
        file_menu.addAction(self.toolbar.save_as_action)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Відкрити", "", "BMP Images (*.bmp)")

        if not file_path:
            return

        try:
            self.document.load(file_path)
            self.viewer.display_image(self.document.get_image())
            self.toolbar.set_image_actions_enabled(True)
            self.statusBar().showMessage(f"Відкрито: {file_path}")

        except Exception as error:
            QMessageBox.critical(self, "Помилка відкриття", str(error))

    def save_image(self):
        if not self.document.is_loaded():
            QMessageBox.warning(self, "Увага", "Спочатку відкрийте зображення")
            return

        if self.document.file_path is None:
            self.save_image_as()
            return

        self.write_to_file(self.document.file_path)

    def save_image_as(self):
        if not self.document.is_loaded():
            QMessageBox.warning(self, "Увага", "Спочатку відкрийте зображення")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Записати як", "", "BMP Images (*.bmp)")

        if not file_path:
            return

        self.write_to_file(file_path)

    def write_to_file(self, file_path):
        try:
            self.document.save(file_path)
            self.statusBar().showMessage(f"Записано: {self.document.file_path}")

        except Exception as error:
            QMessageBox.critical(self, "Помилка запису", str(error))

    def on_mode_changed(self, mode):
        self.statusBar().showMessage(f"Режим: {MODE_NAMES[mode]}")
