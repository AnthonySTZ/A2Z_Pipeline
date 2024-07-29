import os
from PySide2.QtWidgets import QDialog, QVBoxLayout, QApplication
from PySide2 import QtCore, QtUiTools

PROJECT_PATH = "A:/Programming/A2Z_Pipeline/test"


class MainWindow(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)

        self.init_maya_ui("interface\\save_as.ui")
        self.projects_path = PROJECT_PATH

    def show_window(self) -> None:
        self.resize(798, 161)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.update_shots_list()
        self.update_kind_list()
        self.ui.cb_project.currentIndexChanged.connect(self.update_shots_list)
        self.ui.cb_type.currentIndexChanged.connect(self.update_kind_list)

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

    def update_projects_list(self) -> None:
        """Populate project list combo box with available projects from the projects path"""
        self.ui.cb_project.clear()
        if not os.path.exists(self.projects_path):
            print("Invalid projects path")
            return
        project_names = [
            project.name
            for project in os.scandir(self.projects_path)
            if os.path.isdir(os.path.join(self.projects_path, project))
        ]
        for project_name in project_names:
            self.ui.cb_project.addItem(project_name)

    def update_shots_list(self) -> None:
        """Populate shot list combo box with available shots from the selected project"""
        selected_project = self.ui.cb_project.currentText()
        if selected_project == "":
            return
        project_path = os.path.join(self.projects_path, selected_project)
        if not os.path.exists(project_path):
            print(f"Project '{selected_project}' not found")
            return
        shots = [
            shot.name
            for shot in os.scandir(os.path.join(project_path, "40_shots"))
            if shot.is_dir()
        ]
        self.ui.cb_shot.clear()
        for shot in shots:
            self.ui.cb_shot.addItem(shot)

    def update_kind_list(self) -> None:
        """Populate kind list combo box with available kinds"""
        self.ui.cb_kind.clear()
        kinds = {
            "ASSETS": ["MODEL", "GROOM", "ANIM", "SHADING", "MUSCLE"],
            "SHOTS": ["ANIM", "FX", "LIGHT", "RENDER"],
            "RND": ["MODEL", "GROOM", "ANIM", "SHADING", "LIGHT", "MUSCLE"],
        }
        type = self.ui.cb_type.currentText()
        for kind in kinds[type]:
            self.ui.cb_kind.addItem(kind)
