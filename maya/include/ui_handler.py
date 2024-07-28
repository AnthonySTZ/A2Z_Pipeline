import os
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QApplication
from PySide2 import QtCore, QtUiTools


class MainWindow(QMainWindow):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)

        self.init_maya_ui("interface\\save_as.ui")

    def show_window(self) -> None:
        self.resize(896, 282)
        self.show()

    def init_maya_ui(self, uiRelativePath) -> None:
        loader = QtUiTools.QUiLoader()
        dirname = os.path.dirname(__file__)
        uiFilePath = os.path.join(dirname, uiRelativePath)
        uifile = QtCore.QFile(uiFilePath)
        uifile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uifile)
        self.centralLayout = QVBoxLayout(self)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.addWidget(self.ui)
