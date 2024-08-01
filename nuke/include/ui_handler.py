import os
from PySide2.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QApplication,
    QMessageBox,
    QFileDialog,
    QTableWidgetItem,
    QHeaderView,
    QWidget,
    QCheckBox,
    QHBoxLayout,
    QComboBox,
)
from PySide2 import QtCore, QtUiTools
from include.project_handler import ProjectHandler
import nuke


PROJECT_PATH = "A:/Programming/A2Z_Pipeline/test"


class ImportNuke(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)
        self.init_mari_ui("interface\\nuke_import.ui")
        self.projects_path = PROJECT_PATH
        self.project = None

    def show_window(self) -> None:
        self.resize(600, 76)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.selected_project_changed()
        self.update_name_list()
        self.ui.cb_project.currentIndexChanged.connect(self.selected_project_changed)
        self.ui.cb_shot.currentIndexChanged.connect(self.update_name_list)
        self.ui.pb_import.clicked.connect(self.import_sequence)

    def update_projects_list(self):
        self.ui.cb_project.clear()
        if not os.path.exists(self.projects_path):
            QMessageBox.information(self, "Error", "Invalid projects path")
            return
        project_names = [
            project.name
            for project in os.scandir(self.projects_path)
            if os.path.isdir(os.path.join(self.projects_path, project))
        ]
        self.ui.cb_project.addItems(project_names)

    def selected_project_changed(self) -> None:
        """Update save path label with the selected project, shot, and kind"""
        selected_project = self.ui.cb_project.currentText()
        if selected_project == "":
            self.project = None
            return
        project_path = os.path.join(self.projects_path, selected_project)
        if not os.path.exists(project_path):
            print(f"Project '{selected_project}' not found")
            return
        self.project = ProjectHandler(project_path)
        self.update_shots_list()

    def update_shots_list(self) -> None:
        """Populate shot list combo box with available shots from the selected project"""
        if self.project is None:
            return
        shots = self.project.get_all_shots()
        self.ui.cb_shot.clear()
        for shot in shots:
            self.ui.cb_shot.addItem("s" + shot.number + "_" + shot.name)

    def update_name_list(self) -> None:
        """Update the name label with the selected shot"""
        selected_shot = self.ui.cb_shot.currentText()
        if selected_shot == "":
            self.ui.cb_name.clear()
            return

    def import_sequence(self) -> None:
        pass

    def init_mari_ui(self, ui_relative_path) -> None:
        loader = QtUiTools.QUiLoader()
        dirname = os.path.dirname(__file__)
        ui_file_path = os.path.join(dirname, ui_relative_path)
        ui_file = QtCore.QFile(ui_file_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.addWidget(self.ui)


def open_window(window_class):
    window = window_class()
    window.show_window()
