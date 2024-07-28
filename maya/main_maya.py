import sys
import maya.cmds as cmds

PLUGIN_PATH = "A:\\Programming\\A2Z_Pipeline\\maya\\"
sys.path.insert(0, PLUGIN_PATH)

from importlib import reload
import main
import include.project_handler

reload(include.project_handler)
reload(main)
main.start_program()
