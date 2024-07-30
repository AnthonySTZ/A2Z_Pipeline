from include.ui_handler import SaveAs, Save, Open
from maya import OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QApplication, QWidget, QDialog


def create_window(dialog: QDialog):
    if QApplication.instance():
        # Id any current instances of tool and destroy
        for win in QApplication.allWindows():
            if "SaveAs" in win.objectName():  # update this name to match name below
                win.destroy()

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    dialog.window = dialog(parent=mayaMainWindow)
    dialog.window.setObjectName(
        "SaveAs"
    )  # code above uses this to ID any existing windows
    dialog.window.setWindowTitle("A2Z SaveAs")
    dialog.window.show_window()


def openWindow(type: str):
    """
    ID Maya and attach tool window.
    """

    filename = cmds.file(q=True, sn=True)

    if type == "Save":
        if filename:
            create_window(Save)
        else:
            create_window(SaveAs)

    elif type == "Open":
        create_window(Open)
