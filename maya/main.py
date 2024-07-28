from include.project_handler import ProjectHandler
from include.ui_handler import MainWindow
import maya.cmds as cmds
import os
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget


def start_program():

    project_path = "A:/Programming/A2Z_Pipeline/a2z_pipeline/test/TestProject"
    project = ProjectHandler(project_path)
    print(project.name)


def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QApplication.instance():
        # Id any current instances of tool and destroy
        for win in QApplication.allWindows():
            if "SaveAs" in win.objectName():  # update this name to match name below
                win.destroy()

    # QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    MainWindow.window = MainWindow(parent=mayaMainWindow)
    MainWindow.window.setObjectName(
        "SaveAs"
    )  # code above uses this to ID any existing windows
    MainWindow.window.setWindowTitle("A2Z SaveAs")
    MainWindow.window.show_window()
