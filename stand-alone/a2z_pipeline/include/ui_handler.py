from PySide6.QtWidgets import QMainWindow, QInputDialog, QDialog, QTableWidgetItem
from PySide6 import QtUiTools, QtCore
from include.interface.main_window import Ui_MainWindow as UiMainWindow
from include.interface.add_shot_dialog import Ui_Dialog as UiAddShotDialog
import os
from include.project_handler import ProjectHandler

PROJECTS_PATH = "A:/Programming/A2Z_Pipeline/test"


class AddShotDialog(QDialog):
    def __init__(self,  shots:list, parent=None) -> None:
        super().__init__(parent)
        self.ui = UiAddShotDialog()
        self.ui.setupUi(self)
        self.shots = shots
        self.status = False

        self.init_ui()

    def init_ui(self) -> None:
        self.ui.pb_ok.clicked.connect(self.accepted_button_event)
        self.ui.pb_cancel.clicked.connect(self.rejected_button_event)

    def accepted_button_event(self) -> None:
        shot_name = self.ui.le_shot_name.text()
        if shot_name == "":
            print("Please enter a Shot Name")
            return
        
        shot_number = self.ui.sb_shot_number.text().zfill(4)
        if shot_number in self.shots:
            print("Shot number already exists")
            return 

        self.status = True
        self.close()

    def rejected_button_event(self) -> None:
        self.close()

class MainWindow(QMainWindow):
    def __init__(self,parent=None) -> None:
        super().__init__(parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.current_project = None

        self.init_ui()
        self.update_project()
        self.update_shots_table()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.ui.cb_projects.currentIndexChanged.connect(self.update_project)
        self.ui.pb_add_projects.clicked.connect(self.add_project)
        self.ui.pb_add_shot.clicked.connect(self.add_shot)

    def update_projects_list(self):
        if not os.path.exists(PROJECTS_PATH):
            print("Projects path not found")
            return

        projects_list = [f.name for f in os.scandir(PROJECTS_PATH) if f.is_dir()]
        self.ui.cb_projects.clear()
        for project in projects_list:
            self.ui.cb_projects.addItem(project)

    def update_project(self) -> None:
        selected_project_name = self.ui.cb_projects.currentText()
        if selected_project_name == "":
            return
        project_path = os.path.join(PROJECTS_PATH, selected_project_name)
        if not os.path.exists(project_path):
            print(f"Project '{selected_project_name}' not found")
            return

        self.current_project = ProjectHandler(project_path)
        print(f"Project : <{self.current_project.name}> is selected")
        self.update_shots_table()

    def add_project(self) -> None:
        project_name, ok = QInputDialog.getText(
            self, "Add Project", "Enter project name:"
        )
        if ok and project_name:
            project_path = os.path.join(PROJECTS_PATH, project_name)
            if not os.path.exists(project_path):
                ProjectHandler(project_path).init_folders()
                print(f"Project '{project_name}' added successfully")
                self.update_projects_list()

    def add_shot_dialog(self) -> dict | None:
        shot_dialog = AddShotDialog(self.current_project.get_all_shots_number())
        shot_dialog.exec()
        if not shot_dialog.status:
            return None

        shot_name = shot_dialog.ui.le_shot_name.text()
        shot_number = shot_dialog.ui.sb_shot_number.text().zfill(4)
        return {"shot_name": shot_name, "shot_number": shot_number}

    def add_shot(self) -> None:
        if not self.current_project:
            print("No project selected")
            return

        shot_info = self.add_shot_dialog()
        if not shot_info:
            return
        
        self.current_project.add_shot(shot_info["shot_name"], shot_info["shot_number"])
        print(
            f"Added Shot : '{shot_info["shot_name"]}' - '{shot_info["shot_number"]}' to project <{self.current_project.name}>"
        )
        self.update_shots_table()

    def update_shots_table(self) -> None:
        if not self.current_project:
            return
        
        shots = self.current_project.get_all_shots()
        self.ui.tw_shots.setRowCount(0) # Clear the table
        for shot in shots:
            rowPosition = self.ui.tw_shots.rowCount()
            self.ui.tw_shots.insertRow(rowPosition)
            self.ui.tw_shots.setItem(rowPosition, 0, QTableWidgetItem(shot.number))
            self.ui.tw_shots.setItem(rowPosition, 1, QTableWidgetItem(shot.name))
            self.ui.tw_shots.setItem(rowPosition, 2, QTableWidgetItem(shot.thumbnail))
            self.ui.tw_shots.setItem(rowPosition, 3, QTableWidgetItem(shot.description))
        
