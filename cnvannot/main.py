# Annotator - backend

import sys
import tkinter as tk

from cnvannot.common.coordinates import coordinates_from_string
from cnvannot.gui.local.simple_local import LocalGui
from cnvannot.gui.web.simple_web import run_server
from instructions import instructions_show

print("CNV-Annot")

query = None
if len(sys.argv) == 1:
    # Interactive mode
    instructions_show()
    query = coordinates_from_string(input('Please enter a query: '))
else:
    if sys.argv[1] == "gui":
        # Tk GUI
        root = tk.Tk()
        root.title('CNV-Annot')
        gui = LocalGui(root)
        gui.mainloop()
    elif sys.argv[1] == "web-gui":
        # Web GUI
        run_server()
    else:
        # CMD-Line mode
        query = coordinates_from_string(sys.argv[1])
        if query is None:
            print("Something went wrong!")
            exit(1)

print("END")
