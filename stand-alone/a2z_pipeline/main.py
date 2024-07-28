from include.project_handler import ProjectHandler
from include.ui_handler import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":

    project_path = "A:/Programming/A2Z_Pipeline/a2z_pipeline/test/TestProject"
    # project = ProjectHandler(project_path)
    # print(f"Initialize Project : {project.name}")
    # project.init_folders()

    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())
