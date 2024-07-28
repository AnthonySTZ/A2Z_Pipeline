from PySide2.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

    def show_window(self) -> None:
        self.resize(890, 550)
        self.show()
