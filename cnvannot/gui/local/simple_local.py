import tkinter as tk
import webbrowser
from cnvannot.common.coordinates import coordinates_from_string
from tkinter import messagebox
from cnvannot.annotations.ucsc import ucsc_get_annotation_link


class LocalGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.coord = tk.StringVar()
        self.coord.set('hg19:chr2:1000000-2000000:gain')

        self.coord_lbl = tk.Label(text='Genomic Coordinates:\n<ref>:<chr>:<start>-<stop>:<gain|loss>')
        self.coord_lbl.pack()
        self.coord_txt = tk.Entry(textvariable=self.coord)
        self.coord_txt.pack()

        self.ucsc_link = tk.Label(fg="blue", cursor="hand2")
        self.ucsc_link.pack()

        self.res_lbl = tk.Label(text="Press Go to analyze.")
        self.res_lbl.pack()

        self.go_btn = tk.Button(text="GO", command=self.analyze)
        self.go_btn.pack()

        self.reset_btn = tk.Button(text="Reset", command=self.reset)
        self.reset_btn.pack()

    def analyze(self):
        try:
            query = coordinates_from_string(self.coord.get())
        except IndexError:
            tk.messagebox.showinfo('Sorry', 'Malformed query.')
            return

        ucsc_url = str(ucsc_get_annotation_link(query)['ucsc']['link'])
        self.ucsc_link['text'] = 'UCSC'
        self.ucsc_link.bind("<Button-1>", lambda e: self.url_callback(ucsc_url))
        self.res_lbl['text'] = ""  # TODO

    @staticmethod
    def url_callback(url):
        webbrowser.open_new(url)

    def reset(self):
        self.res_lbl['text'] = 'Press Go to analyze.'
        pass
