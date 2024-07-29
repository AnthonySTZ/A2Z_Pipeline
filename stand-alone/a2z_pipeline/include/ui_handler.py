from PySide6.QtWidgets import QMainWindow, QInputDialog, QDialog, QTableWidgetItem, QHeaderView, QCheckBox, QWidget, QHBoxLayout
from PySide6 import QtUiTools, QtCore
from include.interface.main_window import Ui_MainWindow as UiMainWindow
from include.interface.add_shot_dialog import Ui_Dialog as UiAddShotDialog
import os
from include.project_handler import ProjectHandler, Shot

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
        self.shot_name = self.ui.le_shot_name.text()
        if self.shot_name == "":
            print("Please enter a Shot Name")
            return
        
        self.shot_number = "s" + self.ui.sb_shot_number.text().zfill(4)
        if self.shot_number in self.shots:
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
        self.show()

    def init_ui(self) -> None:
        self.init_shots_table_ui()
        self.update_projects_list()
        self.ui.tw_shots.itemChanged.connect(self.shot_item_changed)
        self.ui.cb_projects.currentIndexChanged.connect(self.update_project)
        self.ui.pb_add_projects.clicked.connect(self.add_project)
        self.ui.pb_add_shot.clicked.connect(self.add_shot)

    def init_shots_table_ui(self) -> None:
        self.ui.tw_shots.resizeColumnToContents(0)
        self.ui.tw_shots.resizeColumnToContents(1)
        self.ui.tw_shots.resizeColumnToContents(2)
        self.ui.tw_shots.resizeColumnToContents(3)
        self.ui.tw_shots.resizeColumnToContents(4)
        self.ui.tw_shots.resizeColumnToContents(5)
        self.ui.tw_shots.resizeColumnToContents(6)
        self.ui.tw_shots.resizeColumnToContents(7)
        self.ui.tw_shots.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)

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

        return {"shot_name": shot_dialog.shot_name, "shot_number": shot_dialog.shot_number}

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

    def create_tableWidgetItem(self, value:str, read_only:bool = True)-> QTableWidgetItem:
        item = QTableWidgetItem(value)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if read_only:
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        return item

    def create_tableWidgetCheckboxItem(self, shot:Shot, department:str)-> QWidget:
        checkbox_widget = QWidget()
        checkbox = QCheckBox()
        checkbox.setChecked(bool(shot.departments[department]))
        checkbox.stateChanged.connect(lambda state, shot=shot, department=department: self.toggle_department_shot_state(state, shot, department))
        layout = QHBoxLayout(checkbox_widget)
        layout.addWidget(checkbox)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        return checkbox_widget

    def toggle_department_shot_state(self, state:bool, shot:Shot, department:str)->None:
        shot.departments[department] = bool(state)
        shot.save()

    def create_shot_row(self, shot:Shot)->None:
        rowPosition = self.ui.tw_shots.rowCount()
        self.ui.tw_shots.insertRow(rowPosition)
        number_item = self.create_tableWidgetItem(shot.number)
        name_item = self.create_tableWidgetItem(shot.name)
        thumbnail_item = self.create_tableWidgetItem(shot.thumbnail)
        description_item = self.create_tableWidgetItem(shot.description, read_only=False)
        self.ui.tw_shots.setItem(rowPosition, 0, number_item)
        self.ui.tw_shots.setItem(rowPosition, 1, name_item)
        self.ui.tw_shots.setItem(rowPosition, 2, thumbnail_item)
        for i, department in enumerate(shot.departments):
            checkbox_widget = self.create_tableWidgetCheckboxItem(shot, department)
            self.ui.tw_shots.setCellWidget(rowPosition, i+3, checkbox_widget)
        self.ui.tw_shots.setItem(rowPosition, 8, description_item)

    def update_shots_table(self) -> None:
        if not self.current_project:
            return
        
        shots = self.current_project.get_all_shots()
        self.ui.tw_shots.setRowCount(0) # Clear the table
        for shot in shots:
            self.create_shot_row(shot)
        
        self.init_shots_table_ui()

    def shot_item_changed(self, item:QTableWidgetItem)->None:
        if item.column() == 8:
            shot_number = item.tableWidget().item(item.row(), 0).text()
            new_description = item.text()
            shot = self.current_project.get_shot_by_number(shot_number)
            shot.description = new_description
            shot.save()
