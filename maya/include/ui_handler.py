import os
from PySide2.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QApplication,
    QMessageBox,
    QFileDialog,
)
from PySide2 import QtCore, QtUiTools
from PySide2.QtGui import QPixmap
from include.project_handler import ProjectHandler
import maya.cmds as cmds
import maya.mel as mel
import tempfile
import shutil
import datetime

PROJECT_PATH = "A:/Programming/A2Z_Pipeline/test"


class SaveAs(QDialog):
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
        self.remove_tmp_thumbnail()
        self.ui.cb_project.currentIndexChanged.connect(self.selected_project_changed)
        self.ui.cb_type.currentIndexChanged.connect(self.update_kind_list)
        self.ui.cb_kind.currentIndexChanged.connect(self.update_path)
        self.ui.pb_save.clicked.connect(self.save_as)
        self.ui.pb_screenshot.clicked.connect(self.take_screenshot)
        self.ui.pb_browse.clicked.connect(self.browse_thumbnail)

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
            "ASSETS": ["MODEL", "RIGGING" "GROOM", "ANIM", "SHADING", "MUSCLE"],
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
        selected_type = self.ui.cb_type.currentText()
        selected_kind = self.ui.cb_kind.currentText()
        if self.project is None or selected_shot == "" or selected_kind == "":
            self.ui.l_path.setText("")
            return
        type_folder = {
            "ASSETS": "30_assets",
            "SHOTS": "40_shots",
            "RND": "10_preprod/rnd",
        }
        self.scene_name = (
            type_folder[selected_type]
            + "/"
            + selected_shot
            + "/"
            + selected_kind
            + "/"
            + "WORK/"
            + selected_shot
            + "_"
            + selected_kind
            + "_v001.mb"
        )
        self.ui.l_path.setText(self.scene_name)

    def save_as(self) -> None:
        """Save the current scene to the specified path"""
        if self.project is None or self.scene_name == "":
            print("Invalid project or scene name")
            return

        # Print the save message and the full path to the saved scene
        #
        scene_path = os.path.join(
            self.projects_path, self.project.name, self.scene_name
        ).replace("\\", "/")

        if not os.path.exists(os.path.join(self.projects_path, self.project.name)):
            print("Folder does not exist")
            return

        if os.path.exists(scene_path):
            print(f"Scene already exists at {scene_path}")
            if not self.overwrite_scene():
                return
        print(f"Saving scene to {scene_path}")
        scene_folders_path = scene_path[: -scene_path[::-1].find("/")]
        os.makedirs(scene_folders_path, exist_ok=True)  # Create missing folders
        cmds.file(rename=scene_path)
        cmds.file(save=True)
        self.save_thumbnail()
        self.close()

    def save_thumbnail(self) -> None:
        """Create a thumbnail of the current scene"""
        if not self.thumbnail_path:
            return
        if not os.path.exists(self.thumbnail_path):
            return

        path = self.create_thumbnail_path()

        shutil.copy2(self.thumbnail_path, path)

    def overwrite_scene(self) -> bool:
        """Ask the user if they want to overwrite an existing scene"""
        reply = QMessageBox.question(
            self,
            "Confirm overwrite",
            f"A scene named '{os.path.basename(self.scene_name)}' already exists. Do you want to overwrite it?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    def create_thumbnail_path(self) -> str:
        scene_path = os.path.join(
            self.projects_path, self.project.name, self.scene_name
        ).replace("\\", "/")[:-3]
        scene_folders_path = scene_path[: -scene_path[::-1].find("/")] + "thumbnails/"
        os.makedirs(scene_folders_path, exist_ok=True)
        scene_name = scene_path[-scene_path[::-1].find("/") :]
        path = scene_folders_path + scene_name + ".jpg"
        return path

    def take_screenshot(self) -> None:
        """Take a screenshot of the current scene"""
        scene_path = os.path.join(
            self.projects_path, self.project.name, self.scene_name
        ).replace("\\", "/")[:-3]
        scene_folders_path = scene_path[: -scene_path[::-1].find("/")] + "/thumnails/"
        # os.makedirs(scene_folders_path, exist_ok=True)
        scene_name = scene_path[-scene_path[::-1].find("/") :]
        path = self.create_tmp_path() + "thumbnail_tmp.jpg"
        cmds.playblast(frame=1, cf=path, fmt="iff", orn=0, v=0)
        self.set_thumbnails_image(path)
        self.thumbnail_path = path

    def create_tmp_path(self):
        """
        Return tmp folder path
        """
        path = tempfile.gettempdir() + "\\pipelineThumbnailsTmp\\"
        path = path.replace("\\", "/")
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def browse_thumbnail(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setWindowTitle("Select Thumbnail")
        file_dialog.setNameFilter(("Images (*.png *.xpm *.jpg)"))
        if file_dialog.exec_():
            if file_dialog.selectedFiles():
                file_path = file_dialog.selectedFiles()[0]
                self.thumbnail_path = self.create_tmp_path() + "thumbnail_tmp.jpg"
                shutil.copy2(file_path, self.thumbnail_path)
                self.set_thumbnails_image(self.thumbnail_path)

    def remove_tmp_thumbnail(self) -> None:
        tmp_file = self.create_tmp_path() + "thumbnail_tmp.jpg"
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

    def set_thumbnails_image(self, imagePath):

        pixmap = QPixmap(imagePath).scaledToHeight(90)
        self.ui.l_thumbnail.setPixmap(pixmap)
        self.ui.l_thumbnail.setText("")


class Save(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)
        self.init_maya_ui("interface\\save.ui")
        self.scene_version = None

    def show_window(self) -> None:
        self.resize(798, 132)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_name_and_path()
        self.update_thumbnail()
        self.remove_tmp_thumbnail()
        self.ui.pb_save.clicked.connect(self.save_scene)
        self.ui.pb_add_version.clicked.connect(lambda x: self.add_version(1))
        self.ui.pb_sub_version.clicked.connect(lambda x: self.add_version(-1))
        self.ui.pb_screenshot.clicked.connect(self.take_screenshot)
        self.ui.pb_browse.clicked.connect(self.browse_thumbnail)

    def update_name_and_path(self) -> None:
        """Update save name label with the current scene name"""
        scene_name = cmds.file(query=True, sceneName=True)
        if scene_name is None:
            print("No current scene")
            return
        if self.scene_version is None:
            scene_version = int(scene_name[-6:-3])
            self.scene_version = scene_version
        scene_path = scene_name[:-6] + str(self.scene_version + 1).zfill(3) + ".mb"
        scene_name = scene_path[-scene_path[::-1].find("/") :]
        self.scene_name = scene_name
        self.ui.l_name.setText(scene_name)
        self.ui.l_path.setText(scene_path)

    def update_thumbnail(self) -> None:
        path = self.create_tmp_path() + "thumbnail_tmp.jpg"
        self.set_thumbnails_image(path)

    def add_version(self, num: int) -> None:
        if self.scene_version + num >= 0:
            self.scene_version += num
        self.update_name_and_path()
        self.update_thumbnail()

    def save_scene(self) -> None:
        """Save the current scene to the specified path"""
        scene_path = self.ui.l_path.text()
        if scene_path == "":
            print("Invalid scene path")
            return

        if os.path.exists(scene_path):
            print(f"Scene already exists at {scene_path}")
            if not self.overwrite_scene():
                return

        cmds.file(rename=scene_path)
        cmds.file(save=True)
        self.save_thumbnail()
        self.close()

    def save_thumbnail(self) -> None:
        """Create a thumbnail of the current scene"""
        if not self.thumbnail_path:
            return
        if not os.path.exists(self.thumbnail_path):
            return
        path = self.create_thumbnail_path()
        shutil.copy2(self.thumbnail_path, path)

    def overwrite_scene(self) -> bool:
        """Ask the user if they want to overwrite an existing scene"""
        reply = QMessageBox.question(
            self,
            "Confirm overwrite",
            f"A scene named '{os.path.basename(self.scene_name)}' already exists. Do you want to overwrite it?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    def create_thumbnail_path(self) -> str:
        scene_path = self.ui.l_path.text().replace("\\", "/")[:-3]
        scene_folders_path = scene_path[: -scene_path[::-1].find("/")] + "thumbnails/"
        os.makedirs(scene_folders_path, exist_ok=True)
        scene_name = scene_path[-scene_path[::-1].find("/") :]
        path = scene_folders_path + scene_name + ".jpg"
        return path

    def take_screenshot(self) -> None:
        """Take a screenshot of the current scene"""
        scene_path = self.ui.l_path.text().replace("\\", "/")[:-3]
        scene_folders_path = scene_path[: -scene_path[::-1].find("/")] + "/thumnails/"
        # os.makedirs(scene_folders_path, exist_ok=True)
        scene_name = scene_path[-scene_path[::-1].find("/") :]
        path = self.create_tmp_path() + "thumbnail_tmp.jpg"
        cmds.playblast(frame=1, cf=path, fmt="iff", orn=0, v=0)
        self.set_thumbnails_image(path)
        self.thumbnail_path = path

    def create_tmp_path(self):
        """
        Return tmp folder path
        """
        path = tempfile.gettempdir() + "\\pipelineThumbnailsTmp\\"
        path = path.replace("\\", "/")
        os.makedirs(path, exist_ok=True)

        return path

    def set_thumbnails_image(self, imagePath):
        if not os.path.exists(imagePath):
            self.ui.l_thumbnail.setPixmap(QPixmap())
            return
        pixmap = QPixmap(imagePath).scaledToHeight(90)
        self.ui.l_thumbnail.setPixmap(pixmap)
        self.ui.l_thumbnail.setText("")

    def browse_thumbnail(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setWindowTitle("Select Thumbnail")
        file_dialog.setNameFilter(("Images (*.png *.xpm *.jpg)"))
        if file_dialog.exec_():
            if file_dialog.selectedFiles():
                file_path = file_dialog.selectedFiles()[0]
                self.thumbnail_path = self.create_tmp_path() + "thumbnail_tmp.jpg"
                shutil.copy2(file_path, self.thumbnail_path)
        self.update_thumbnail()

    def remove_tmp_thumbnail(self) -> None:
        tmp_file = self.create_tmp_path() + "thumbnail_tmp.jpg"
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
            self.update_thumbnail()

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


class Open(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)
        self.init_maya_ui("interface\\open.ui")
        self.projects_path = PROJECT_PATH
        self.project = None

    def show_window(self) -> None:
        self.resize(798, 132)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.selected_project_changed()
        self.update_shots_list()
        self.update_kind_list()
        self.update_scene()
        self.ui.cb_project.currentIndexChanged.connect(self.selected_project_changed)
        self.ui.cb_type.currentIndexChanged.connect(self.update_kind_list)
        self.ui.cb_kind.currentIndexChanged.connect(self.update_scene)
        self.ui.cb_scene.currentIndexChanged.connect(self.update_path)
        self.ui.pb_open.clicked.connect(self.open_scene)
        self.ui.pb_ref.clicked.connect(self.open_as_ref)

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
            self.update_scene()
            return
        shots = self.project.get_all_shots()
        self.ui.cb_shot.clear()
        for shot in shots:
            self.ui.cb_shot.addItem("s" + shot.number + "_" + shot.name)

        self.update_scene()

    def update_kind_list(self) -> None:
        """Populate kind list combo box with available kinds"""
        self.ui.cb_kind.clear()
        kinds = {
            "ASSETS": ["MODEL", "RIGGING", "GROOM", "ANIM", "SHADING", "MUSCLE"],
            "SHOTS": ["ANIM", "FX", "LIGHT", "RENDER"],
            "RND": ["MODEL", "GROOM", "ANIM", "SHADING", "LIGHT", "MUSCLE"],
        }
        type = self.ui.cb_type.currentText()
        for kind in kinds[type]:
            self.ui.cb_kind.addItem(kind)

        self.update_scene()
        self.update_path()

    def update_scene(self) -> None:
        selected_shot = self.ui.cb_shot.currentText()
        selected_type = self.ui.cb_type.currentText()
        selected_kind = self.ui.cb_kind.currentText()
        if self.project is None or selected_shot == "" or selected_kind == "":
            self.ui.l_path.setText("")
            self.ui.cb_scene.clear()
            return
        type_folder = {
            "ASSETS": "30_assets",
            "SHOTS": "40_shots",
            "RND": "10_preprod/rnd",
        }
        self.scenes_path = (
            self.project.path
            + "/"
            + type_folder[selected_type]
            + "/"
            + selected_shot
            + "/"
            + selected_kind
            + "/WORK"
        )
        self.ui.cb_scene.clear()
        if not os.path.exists(self.scenes_path):
            return
        files = [f.name for f in os.scandir(self.scenes_path)][::-1]
        for file in files:
            if file != "thumbnails":
                self.ui.cb_scene.addItem(file)

    def get_scene_path(self) -> str:
        selected_scene = self.ui.cb_scene.currentText()
        if selected_scene == "":
            return ""
        return os.path.join(self.scenes_path, selected_scene).replace("\\", "/")

    def update_path(self) -> None:
        """Update save path label with the selected scene path"""
        selected_scene = self.get_scene_path()
        self.ui.l_path.setText(selected_scene)
        self.update_scene_infos()
        self.update_thumbnail()

    def update_scene_infos(self) -> None:
        selected_scene = self.get_scene_path()
        if selected_scene == "":
            self.ui.l_date.setText("")
            self.ui.l_size.setText("")
            return
        scene_infos = os.stat(selected_scene)
        self.ui.l_date.setText(
            str(datetime.datetime.fromtimestamp(scene_infos.st_mtime))[:-7]
        )
        self.ui.l_size.setText("%.2f" % (scene_infos.st_size / (1024 * 1024)) + " MB")

    def open_scene(self) -> None:
        """Open the selected scene in Maya"""
        selected_scene = self.get_scene_path()
        if selected_scene == "":
            print("Invalid scene path")
            return
        cmds.file(selected_scene, open=True, force=True)
        self.close()

    def open_as_ref(self) -> None:
        """Open the selected scene in Maya as a reference"""
        selected_scene = self.get_scene_path()
        if selected_scene == "":
            print("Invalid scene path")
            return
        cmds.file(selected_scene, reference=True, force=True)
        self.close()

    def update_thumbnail(self) -> None:
        path = self.create_thumbnail_path()
        self.set_thumbnails_image(path)

    def create_thumbnail_path(self) -> str:
        scene_path = self.ui.l_path.text().replace("\\", "/")[:-3]
        scene_folders_path = scene_path[: -scene_path[::-1].find("/")] + "thumbnails/"
        os.makedirs(scene_folders_path, exist_ok=True)
        scene_name = scene_path[-scene_path[::-1].find("/") :]
        path = scene_folders_path + scene_name + ".jpg"
        return path

    def set_thumbnails_image(self, imagePath):
        if not os.path.exists(imagePath):
            self.ui.l_thumbnail.setPixmap(QPixmap())
            return
        pixmap = QPixmap(imagePath).scaledToHeight(90)
        self.ui.l_thumbnail.setPixmap(pixmap)
        self.ui.l_thumbnail.setText("")

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


class ExportMesh(QDialog):

    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)
        self.init_maya_ui("interface\\export_mesh.ui")
        self.projects_path = PROJECT_PATH
        self.project = None

    def show_window(self) -> None:
        self.resize(798, 132)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.update_project()
        self.update_kind_list()
        self.ui.cb_project.currentIndexChanged.connect(self.selected_project_changed)
        self.ui.cb_type.currentIndexChanged.connect(self.update_kind_list)
        self.ui.pb_export.clicked.connect(self.export_mesh)

    def update_projects_list(self) -> None:
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

    def update_project(self) -> None:
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
        if self.project is None:
            self.update_scene()
            return
        shots = self.project.get_all_shots()
        self.ui.cb_shot.clear()
        for shot in shots:
            self.ui.cb_shot.addItem("s" + shot.number + "_" + shot.name)

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

    def get_mesh_path(self) -> str:
        selected_shot = self.ui.cb_shot.currentText()
        selected_type = self.ui.cb_type.currentText()
        selected_kind = self.ui.cb_kind.currentText()
        selected_format = self.ui.cb_format.currentText()
        mesh_name = self.ui.le_name.text()
        if (
            self.project is None
            or selected_shot == ""
            or selected_kind == ""
            or mesh_name == ""
        ):
            print("Invalid selection")
            return None
        type_folder = {
            "ASSETS": "30_assets",
            "SHOTS": "40_shots",
            "RND": "10_preprod/rnd",
        }
        mesh_path = (
            self.project.path
            + "/"
            + type_folder[selected_type]
            + "/"
            + selected_shot
            + "/"
            + selected_kind
            + "/"
            + "EXPORT/"
            + selected_shot
            + "_"
            + selected_kind
            + "_"
            + mesh_name
            + selected_format
        )
        return mesh_path

    def export_mesh(self) -> None:
        """Export selected scene mesh to specified path"""
        export_path = self.get_mesh_path()
        if export_path is None:
            return
        export_folders = export_path[: -export_path[::-1].find("/")]
        os.makedirs(export_folders, exist_ok=True)
        format = self.ui.cb_format.currentText()
        if format == ".obj":
            cmds.file(
                export_path,
                exportSelected=self.ui.cb_export_selected.isChecked(),
                type="OBJexport",
                op="groups=0; ptgroups=0;materials=0; smoothing=0; normals=0",
                force=True,
            )
        elif format == ".fbx":
            if self.ui.cb_export_selected.isChecked():
                mel.eval('FBXExport -f "{0}" -s'.format(export_path))
            else:
                mel.eval('FBXExport -f "{0}"'.format(export_path))
        self.close()

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
