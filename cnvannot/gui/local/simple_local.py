import tkinter as tk
import webbrowser
from cnvannot.common.coordinates import coordinates_from_string
from tkinter import messagebox
from cnvannot.annotations.ucsc import ucsc_get_annotation_link
from cnvannot.annotations.xcnv import xcnv_predict, xcnv_interpretation_from_score


class LocalGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.coord = tk.StringVar()
        self.coord.set('hg19:chr2:1000000-2000000:gain')

        self.coord_lbl = tk.Label(text='Genomic Coordinates:\n\n<ref>:<chr>:<start>-<stop>:<gain|loss>\n')
        self.coord_lbl.pack()
        self.coord_txt = tk.Entry(textvariable=self.coord, width=40)
        self.coord_txt.pack()

        self.ucsc_link = tk.Label(fg="blue", cursor="hand2")
        self.ucsc_link.pack()

        self.res_lbl = tk.Label(text="Press Go to analyze.")
        self.res_lbl.pack()

        self.go_btn = tk.Button(text="GO", width=20, command=self.analyze)
        self.go_btn.pack()

        self.reset_btn = tk.Button(text="Reset", width=20, command=self.reset)
        self.reset_btn.pack()

    def analyze(self):
        try:
            query = coordinates_from_string(self.coord.get())
        except IndexError:
            tk.messagebox.showinfo('Sorry', 'Malformed query.')
            return

        self.res_lbl['text'] = 'Please wait...'

        # UCSC
        ucsc_url = str(ucsc_get_annotation_link(query)['ucsc']['link'])
        self.ucsc_link['text'] = 'UCSC'
        self.ucsc_link.bind("<Button-1>", lambda e: self.url_callback(ucsc_url))

        # X-CNV
        xcnv_res = xcnv_predict(query)['xcnv']['prediction']

        self.res_lbl['text'] = 'X-CNV: ' + "{:1.2f}".format(xcnv_res) + ' (' + xcnv_interpretation_from_score(xcnv_res) + ')'

        # TODO: Add other annotations.

    @staticmethod
    def url_callback(url):
        webbrowser.open_new(url)

    def reset(self):
        self.res_lbl['text'] = 'Press Go to analyze.'
        pass
