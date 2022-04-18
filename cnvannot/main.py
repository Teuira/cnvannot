# Annotator - backend

import sys
import tkinter as tk

from instructions import instructions_show
from cnvannot.annotations.dgv import dgv_gold_load
from cnvannot.annotations.refseq import refseq_load
from cnvannot.annotations.omim import omim_morbid_genes_load
from cnvannot.annotations.encode import encode_load
from cnvannot.annotations.xcnv import xcnv_is_avail
from cnvannot.common.coordinates import coordinates_from_string
from cnvannot.gui.local.simple_local import LocalGui

print("CNVAnnot")

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
        pass
    else:
        # CMD-Line mode
        query = coordinates_from_string(sys.argv[1])

if query is None:
    print("Something went wrong!")
    exit(1)

# DBs loading
print('Loading DBs...')
dgv_db = dgv_gold_load()
refseq_db = refseq_load()
omim_mg_db = omim_morbid_genes_load()
encode_db = encode_load()
print("XCNV is available" if xcnv_is_avail() else "XCNV is NOT available")
print('...DBs loaded!')

# DGV Querying
if query.chr in dgv_db:
    if dgv_db[query.chr].overlaps(query.start, query.end):
        print("Overlap(s) found in DGV")
        with open("out.json", "a") as out_file:
            out_file.write('{')
        for r in dgv_db[query.chr][query.start:query.end]:
            t = r.data['var_type']
            if t != query.type:
                continue
            if r.data['freq'] < 1:
                print("< 1%: " + str(r))
            else:
                print(">= 1%: " + str(r))
            with open("out.json", "a") as out_file:
                out_file.write(str(r.data) + ',\n')
        with open("out.json", "a") as out_file:
            out_file.write('}')
    else:
        print("No overlaps found")
else:
    print("Invalid Chromosome name!")

# RefSeq Querying
if query.chr in refseq_db:
    if refseq_db[query.chr].overlaps(query.start, query.end):
        print("Overlap(s) found in RefSeq")
        for r in refseq_db[query.chr][query.start:query.end]:
            print(r.data['name1'] + ' ' + r.data['name2'])
    else:
        print("No overlaps found in RefSeq")
else:
    print("Invalid Chromosome name (" + query.chr + ") !")

print("END")
