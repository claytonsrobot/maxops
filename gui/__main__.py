'''
[Title]:
gui.py
[Author] 
"Clayton Bennett"
[Created] 
date(08 March 2025)

[[Description]]
"""freesimplegui implementation for wateropforms;
try: pip install poetry

run this installation command:
poetry add wateropforms # in powershell, bash, termux, and on. ;
write this python script: #README.md
from wateropforms import wateropforms as wof
print(f"dir(wof) = {dir(wof)}")
"""
[[Purpose]]
"mock up the appearance of the data entry"

'''

import FreeSimpleGUI as sg
from gui.outfall import outfall_window
from gui.hourly import hourly_window

#print(dir(sg))
#sg.user_settings_object
#sg.ttk
#sg.warnings

class GuiApp:
    
    def __init__(self):
        self.vars = {}

    def do_browsefiles(self,args):
        file_path = sg.popup_get_file("Select a filepath to assign to variable!")
        return file_path

    def main(self):
        layout = [
            [sg.Button("Outfall Frame", key="-OUTFALL-"), sg.Button("Hourly Frame", key="-HOURLY-"), sg.Button("Exit", key="-EXIT-")]
        ]

        window = sg.Window("Main Menu", layout)

        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break
            if event == "-OUTFALL-":
                outfall_window()
            if event == "-HOURLY-":
                hourly_window()

        window.close()

if __name__ == "__main__":
    app = GuiApp()
    app.main()
