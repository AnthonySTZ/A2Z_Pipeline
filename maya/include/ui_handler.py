import os
from PySide2.QtWidgets import QDialog, QVBoxLayout, QApplication
from PySide2 import QtCore, QtUiTools

PROJECT_PATH = "A:/Programming/A2Z_Pipeline/a2z_pipeline/test"


class MainWindow(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)

        self.init_maya_ui("interface\\save_as.ui")

    def show_window(self) -> None:
        self.resize(798, 161)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        pass

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
