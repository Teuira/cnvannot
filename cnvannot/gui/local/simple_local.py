import tkinter as tk


class LocalGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.coord_lbl = tk.Label(text="Genomic Coordinates:")
        self.coord_lbl.pack()
        self.coord_txt = tk.Entry()
        self.coord_txt.pack()

        self.go_btn = tk.Button(text="GO", command=self.analyze)
        self.go_btn.pack()

    @staticmethod
    def analyze():
        print("test")
