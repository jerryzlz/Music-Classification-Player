import json
import os
from fct import file, welcome, interface
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("player")

dir_path = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
settings = json.load(open("settings.json", "r"))

first_run = file.first_run(settings["first_run"])
if first_run is True:
    welcome.window()
    settings["first_run"] = "0"
    json.dump(settings, open("settings.json", "w"))

file.create_dir(file.dir_name(dir_path)[1])

app = interface.QtWidgets.QApplication(interface.sys.argv)
win = interface.Index(dir_path, settings)
win.show()
interface.sys.exit(app.exec())
