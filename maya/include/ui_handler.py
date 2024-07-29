import os
from PySide2.QtWidgets import QDialog, QVBoxLayout, QApplication
from PySide2 import QtCore, QtUiTools
from include.project_handler import ProjectHandler

PROJECT_PATH = "A:/Programming/A2Z_Pipeline/test"


class MainWindow(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)

        self.init_maya_ui("interface\\save_as.ui")
        self.projects_path = PROJECT_PATH
        self.project = None

    def show_window(self) -> None:
        self.resize(798, 161)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.selected_project_changed()
        self.update_shots_list()
        self.update_kind_list()
        self.ui.cb_project.currentIndexChanged.connect(self.selected_project_changed)
        self.ui.cb_type.currentIndexChanged.connect(self.update_kind_list)
        self.ui.cb_kind.currentIndexChanged.connect(self.update_path)

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

        self.update_path()

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

        self.update_path()

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

        self.update_path()

    def update_path(self) -> None:
        """Update save path label with the selected project, shot, and kind"""
        selected_shot = self.ui.cb_shot.currentText()
        selected_kind = self.ui.cb_kind.currentText()
        if self.project is None or selected_shot == "" or selected_kind == "":
            self.ui.l_path.setText("")
            return
        self.scene_name = selected_shot + "_" + selected_kind + "_v001.mb"
        self.ui.l_path.setText(self.scene_name)
