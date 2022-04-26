import tkinter as tk
import webbrowser
from tkinter import messagebox

from cnvannot.annotations.dgv import dgv_gold_load
from cnvannot.annotations.encode import encode_load
from cnvannot.annotations.omim import omim_morbid_genes_load
from cnvannot.annotations.refseq import refseq_load
from cnvannot.annotations.ucsc import ucsc_get_annotation_link
from cnvannot.annotations.xcnv import xcnv_is_avail
from cnvannot.annotations.xcnv import xcnv_predict, xcnv_interpretation_from_score
from cnvannot.common.coordinates import coordinates_from_string
from cnvannot.queries.basic_queries import *
from cnvannot.queries.specific_queries import *
from cnvannot.queries.interpretation import *


class LocalGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.dgv_db = None
        self.refseq_db = None
        self.omim_mg_db = None
        self.encode_db = None

        self.load_dbs()

        self.coord = tk.StringVar()
        self.coord.set('hg19:chr2:1000000-2000000:gain')

        self.coord_lbl = tk.Label(text='\nGenomic Coordinates:\n<ref>:<chr>:<start>-<stop>:<gain|loss>\n')
        self.coord_lbl.pack()
        self.coord_txt = tk.Entry(textvariable=self.coord, width=40)
        self.coord_txt.pack()

        self.ucsc_link = tk.Label(fg="blue", cursor="hand2")
        self.ucsc_link.pack()

        self.res_lbl = tk.Label(text="Press GO to analyze.\n")
        self.res_lbl.pack()

        self.go_btn = tk.Button(text="GO", width=20, command=self.analyze, background='green')
        self.go_btn.pack()

        self.reset_btn = tk.Button(text="Reset", width=20, command=self.reset, background='red')
        self.reset_btn.pack()

    def load_dbs(self):
        # DBs loading
        print('Loading DBs...')
        self.dgv_db = dgv_gold_load()
        self.refseq_db = refseq_load()
        self.omim_mg_db = omim_morbid_genes_load()
        self.encode_db = encode_load()
        print("X-CNV is available" if xcnv_is_avail() else "X-CNV is NOT available")
        print('...DBs loaded!')

    def analyze(self):
        try:
            query = coordinates_from_string(self.coord.get())
        except IndexError:
            tk.messagebox.showinfo('Sorry', 'Malformed query.')
            return

        self.res_lbl['text'] = 'Please wait...'

        # UCSC
        ucsc_url = str(ucsc_get_annotation_link(query)['ucsc']['link'])
        self.ucsc_link['text'] = '\nUCSC Web Browser\n'
        self.ucsc_link.bind("<Button-1>", lambda e: self.url_callback(ucsc_url))

        self.res_lbl['text'] = ''
        # Basic infos
        self.res_lbl['text'] += 'CNV length: ' + f'{(query.end - query.start):,}' + ' bases\n'
        self.res_lbl['text'] += 'Type: ' + str.upper(query.type) + '\n'
        # X-CNV
        xcnv_res = xcnv_predict([query])[0]['xcnv']['prediction']
        self.res_lbl['text'] += 'X-CNV: ' + f'{xcnv_res:1.2f}' + ' (' + xcnv_interpretation_from_score(xcnv_res) + ')\n'
        # ENCODE
        exclude_overlaps = query_overlaps(self.encode_db, query)
        self.res_lbl['text'] += 'Intersects excluded regions: ' + str(exclude_overlaps) + '\n '
        # RefSeq
        gene_overlap_count = query_overlap_count(self.refseq_db, query)
        self.res_lbl['text'] += 'Number of genes intersected: ' + str(gene_overlap_count) + '\n'
        # OMIM Morbid genes
        morbid_gene_overlap_count = query_overlap_count(self.omim_mg_db, query)
        self.res_lbl['text'] += 'Overlaps OMIM morbid genes: ' + str(morbid_gene_overlap_count) + '\n'
        dgv_gold_cnv_overlap_count = dgv_gold_overlap_count_1_percent(self.dgv_db, query)
        # DGV Gold >= 1%
        self.res_lbl['text'] += 'Overlaps DGV Gold CNVs: ' + str(dgv_gold_cnv_overlap_count) + '\n'

        # Interpretation
        if xcnv_is_avail():
            self.res_lbl['text'] += '\nInterpretation suggestion(s): ' + interpretation_get(xcnv_res,
                                                                                            exclude_overlaps,
                                                                                            gene_overlap_count,
                                                                                            morbid_gene_overlap_count,
                                                                                            dgv_gold_cnv_overlap_count,
                                                                                            query.type) + '\n'

    @staticmethod
    def url_callback(url):
        webbrowser.open_new(url)

    def reset(self):
        self.ucsc_link['text'] = ''
        self.res_lbl['text'] = 'Press GO to analyze.\n'
        self.coord.set('hg19:')
        pass
