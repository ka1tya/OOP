from enum import Enum
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QDockWidget, QFormLayout, QGroupBox, QLabel, QPushButton, QSlider, QStyle, QToolBar, QVBoxLayout, QWidget

class EditMode(Enum):
    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    RGB = "rgb"

class MainToolBar(QToolBar):
    open_requested = Signal()
    save_requested = Signal()
    save_as_requested = Signal()
    mode_changed = Signal(EditMode)

    def __init__(self, parent=None):
        super().__init__("Панель інструментів", parent)

        self.setMovable(False)
        self.create_file_actions()
        self.addSeparator()
        self.create_mode_actions()
        self.set_image_actions_enabled(False)

    def create_file_actions(self):
        style = self.style()

        self.open_action = self.create_action(
            "Відкрити...",
            "Відкрити BMP-зображення (24 біти)",
            style.standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton),
        )
        self.open_action.triggered.connect(self.open_requested)

        self.save_action = self.create_action(
            "Записати",
            "Записати зображення у поточний файл",
            style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
        )
        self.save_action.triggered.connect(self.save_requested)

        self.save_as_action = self.create_action(
            "Записати як...",
            "Записати зображення у новий BMP-файл",
            style.standardIcon(QStyle.StandardPixmap.SP_DriveFDIcon),
        )
        self.save_as_action.triggered.connect(self.save_as_requested)

        self.addAction(self.open_action)
        self.addAction(self.save_action)
        self.addAction(self.save_as_action)

    def create_mode_actions(self):
        self.mode_group = QActionGroup(self)
        self.mode_group.setExclusive(True)

        self.mode_actions = {
            EditMode.BRIGHTNESS: self.create_action(
                "Світлота", "Режим зміни світлоти зображення"
            ),
            EditMode.CONTRAST: self.create_action(
                "Контраст", "Режим зміни контрасту зображення"
            ),
            EditMode.RGB: self.create_action(
                "Корекція RGB", "Режим корекції компонент R, G, B"
            ),
        }

        for mode, action in self.mode_actions.items():
            action.setCheckable(True)
            action.setData(mode)
            self.mode_group.addAction(action)
            self.addAction(action)

        self.mode_group.triggered.connect(self.on_mode_triggered)

    def create_action(self, text, tooltip, icon=None):
        action = QAction(text, self)

        if icon is not None:
            action.setIcon(icon)

        action.setToolTip(tooltip)
        action.setStatusTip(tooltip)

        return action

    def on_mode_triggered(self, action):
        self.mode_changed.emit(action.data())

    def set_image_actions_enabled(self, enabled):
        self.save_action.setEnabled(enabled)
        self.save_as_action.setEnabled(enabled)
        self.mode_group.setEnabled(enabled)

class AdjustmentPanel(QDockWidget):
    values_changed = Signal()

    DEFAULT_VALUE = 100

    def __init__(self, parent=None):
        super().__init__("Обробка зображення", parent)

        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetClosable
        )

        self.sliders = {}
        self.value_labels = {}

        panel = QWidget()
        layout = QVBoxLayout(panel)

        self.groups = {
            EditMode.BRIGHTNESS: self.create_group(
                "Світлота", [("brightness", "Світлота:")]
            ),
            EditMode.CONTRAST: self.create_group(
                "Контраст", [("contrast", "Контраст:")]
            ),
            EditMode.RGB: self.create_group(
                "Корекція RGB",
                [
                    ("red", "Червоний (R):"),
                    ("green", "Зелений (G):"),
                    ("blue", "Синій (B):"),
                ],
            ),
        }

        for group in self.groups.values():
            layout.addWidget(group)

        reset_button = QPushButton("Скинути налаштування")
        reset_button.setToolTip("Повернути всі параметри до 100%")
        reset_button.clicked.connect(self.reset)

        layout.addWidget(reset_button)
        layout.addStretch()

        self.setWidget(panel)
        self.hide()

    def create_group(self, title, sliders):
        group = QGroupBox(title)
        form = QFormLayout(group)

        for name, label in sliders:
            form.addRow(label, self.create_slider_row(name))

        return group

    def create_slider_row(self, name):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 200)
        slider.setValue(self.DEFAULT_VALUE)

        value_label = QLabel(f"{self.DEFAULT_VALUE}%")
        value_label.setMinimumWidth(40)

        slider.valueChanged.connect(
            lambda value, label=value_label: label.setText(f"{value}%")
        )
        slider.valueChanged.connect(self.values_changed)

        self.sliders[name] = slider
        self.value_labels[name] = value_label

        row = QWidget()
        layout = QVBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(slider)
        layout.addWidget(value_label)

        return row

    def show_mode(self, mode):
        for group_mode, group in self.groups.items():
            group.setVisible(group_mode == mode)

        self.show()

    def values(self):
        return {
            name: slider.value() / 100
            for name, slider in self.sliders.items()
        }

    def reset(self):
        for name, slider in self.sliders.items():
            slider.blockSignals(True)
            slider.setValue(self.DEFAULT_VALUE)
            slider.blockSignals(False)
            self.value_labels[name].setText(f"{self.DEFAULT_VALUE}%")

        self.values_changed.emit()
