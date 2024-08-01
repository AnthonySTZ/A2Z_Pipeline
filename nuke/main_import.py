import sys


def load():

    PLUGIN_PATH = "A:\\Programming\\A2Z_Pipeline\\mari"
    sys.path.insert(0, PLUGIN_PATH)

    from importlib import reload
    import include.project_handler as project_handler
    import include.ui_handler as ui_handler

    reload(project_handler)
    reload(ui_handler)
    ui_handler.open_window(ui_handler.ImportNuke)
