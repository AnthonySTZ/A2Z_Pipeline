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
import mari


PROJECT_PATH = "A:/Programming/A2Z_Pipeline/test"


class MariWindow(QDialog):
    def __init__(self, parent=QApplication.activeWindow()):
        super().__init__(parent)
        self.init_mari_ui("interface\\mari_export.ui")
        self.projects_path = PROJECT_PATH
        self.project = None
        self.export_channel_checkboxes = []
        self.channel_sizes = []
        self.channel_colorspaces = []
        self.channel_depths = []

    def show_window(self) -> None:
        self.resize(600, 400)
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        self.update_projects_list()
        self.selected_project_changed()
        self.update_materials_table()
        self.ui.cb_project.currentIndexChanged.connect(self.selected_project_changed)
        self.ui.pb_export.clicked.connect(self.export_event)

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

    def init_materials_table_ui(self) -> None:
        """Initialize the materials table"""
        self.ui.tw_materials_table.resizeColumnToContents(0)
        self.ui.tw_materials_table.resizeColumnToContents(1)
        self.ui.tw_materials_table.resizeColumnToContents(2)
        self.ui.tw_materials_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.Stretch
        )

    def update_materials_table(self) -> None:
        self.channels = mari.geo.current().channelList()
        self.ui.tw_materials_table.setRowCount(0)  # Clear the table
        for channel in self.channels:
            self.create_material_row(channel)

        self.init_materials_table_ui()

    def create_material_row(self, channel) -> None:
        """Create a new row in the materials table"""
        source_item = self.create_tableWidgetCheckboxItem(channel.name())
        rowPosition = self.ui.tw_materials_table.rowCount()
        self.ui.tw_materials_table.insertRow(rowPosition)
        self.ui.tw_materials_table.setCellWidget(rowPosition, 0, source_item)

        size_item = self.create_table_size_combobox(channel.width())
        self.ui.tw_materials_table.setCellWidget(rowPosition, 1, size_item)

        colorspace_item = self.create_table_colorspace_combobox(channel)
        self.ui.tw_materials_table.setCellWidget(rowPosition, 2, colorspace_item)

        depth_item = self.create_table_depth_combobox(channel)
        self.ui.tw_materials_table.setCellWidget(rowPosition, 3, depth_item)

    def create_tableWidgetCheckboxItem(self, channel_name: str) -> QWidget:
        checkbox_widget = QWidget()
        checkbox = QCheckBox(channel_name)
        checkbox.setChecked(True)
        self.export_channel_checkboxes.append(checkbox)
        layout = QHBoxLayout(checkbox_widget)
        layout.addWidget(checkbox)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(5, 0, 0, 0)
        return checkbox_widget

    def create_table_size_combobox(self, channel_size: int) -> None:
        combobox_widget = QWidget()
        combobox = QComboBox()
        sizes_list = [2**i for i in range(8, 14)]
        combobox.addItem("Same as Source")
        for size in sizes_list:
            size_text = str(size) + "x" + str(size)
            combobox.addItem(size_text)
        self.channel_sizes.append(combobox)
        layout = QHBoxLayout(combobox_widget)
        layout.addWidget(combobox)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(5, 0, 0, 0)
        return combobox_widget

    def create_table_colorspace_combobox(self, channel) -> None:
        combobox_widget = QWidget()
        combobox = QComboBox()
        colorpace_list = channel.colorspaceConfig().availableColorspaces()
        combobox.addItem("Same as Source")
        for colorspace in colorpace_list:
            combobox.addItem(colorspace)
        self.channel_colorspaces.append(combobox)
        layout = QHBoxLayout(combobox_widget)
        layout.addWidget(combobox)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(5, 0, 0, 0)
        return combobox_widget

    def create_table_depth_combobox(self, channel) -> None:
        combobox_widget = QWidget()
        combobox = QComboBox()
        depth_list = ["8 bits (byte)", "16 bits (half)", "32 bits (float)"]
        combobox.addItem("Same as Source")
        for depth in depth_list:
            combobox.addItem(depth)
        self.channel_depths.append(combobox)
        layout = QHBoxLayout(combobox_widget)
        layout.addWidget(combobox)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(5, 0, 0, 0)
        return combobox_widget

    def update_channel_node_by_infos(self, channel, index: int) -> None:
        channel_size = self.channel_sizes[index].currentIndex()
        channel_colorspace = self.channel_colorspaces[index].currentIndex()
        channel_depth = self.channel_depths[index].currentIndex()

        if channel_size != 0:
            sizes_list = [2**i for i in range(8, 14)]
            size = mari.ImageSet.Size(sizes_list[channel_size - 1])
            channel.resize(size)

        if channel_colorspace != 0:
            colorspace_list = channel.colorspaceConfig().availableColorspaces()
            colorspace = colorspace_list[channel_colorspace - 1]
            channel.convertColorspaceTo(colorspace)

        if channel_depth != 0:
            channel_depth_list = [8, 16, 32]
            depth = mari.Image.Depth(channel_depth_list[channel_depth - 1])
            channel.setDepth(depth, mari.Channel.ConvertOption(1))

    def export_event(self) -> None:
        """Export selected materials to the specified location"""
        if self.project is None:
            QMessageBox.information(self, "Error", "No project selected")
            return
        if self.ui.le_name.text() == "":
            QMessageBox.information(self, "Error", "Please enter a name...")
            return
        selected_shot = self.ui.cb_shot.currentText()
        asset_name = self.ui.le_name.text()
        export_path = (
            self.project.path
            + "/30_assets/"
            + selected_shot
            + "/TEXTURES/WORK/"
            + asset_name
        )
        if self.ui.cb_publish.isChecked():
            export_path = export_path.replace("/WORK/", "/PUBLISH/")
        os.makedirs(export_path, exist_ok=True)
        eItems = []
        self.channels = mari.geo.current().channelList()
        for i, channel in enumerate(self.channels):
            if not self.export_channel_checkboxes[i].isChecked():
                continue
            self.update_channel_node_by_infos(channel, i)
            eItem = mari.ExportItem()
            eItem.setSourceNode(channel.channelNode())
            eItem.setFileTemplate("$ENTITY/$CHANNEL.$UDIM.tiff")
            mari.exports.addExportItem(eItem, mari.geo.current())
            eItems.append(eItem)
        mari.exports.exportTextures(eItems, export_path)

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


def open_window():
    window = MariWindow()
    window.show_window()
