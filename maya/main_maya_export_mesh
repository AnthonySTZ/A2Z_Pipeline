import sys
import maya.cmds as cmds

PLUGIN_PATH = "A:\\Programming\\A2Z_Pipeline\\maya\\"
sys.path.insert(0, PLUGIN_PATH)

from importlib import reload
import main
import include.project_handler as project_handler
import include.ui_handler as ui_handler

reload(project_handler)
reload(ui_handler)
reload(main)
main.openWindow("Export_Mesh")
