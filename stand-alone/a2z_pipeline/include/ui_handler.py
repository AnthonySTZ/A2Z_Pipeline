from PySide6.QtWidgets import QMainWindow
from PySide6 import QtUiTools, QtCore
from include.interface.main_window import Ui_MainWindow as UiMainWindow
import os


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.show()
