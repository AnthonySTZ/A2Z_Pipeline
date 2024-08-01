import main_import

menu = nuke.menu("Nuke")
menu.addCommand("A2Z_Pipeline/Import", "main_import.load()")
