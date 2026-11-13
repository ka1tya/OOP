from enum import Enum
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QStyle, QToolBar

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

    def current_mode(self):
        action = self.mode_group.checkedAction()

        if action is None:
            return None

        return action.data()

    def set_image_actions_enabled(self, enabled):
        self.save_action.setEnabled(enabled)
        self.save_as_action.setEnabled(enabled)
        self.mode_group.setEnabled(enabled)
