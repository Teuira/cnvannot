# Annotator - backend

import sys
from dgv import dgv_gold_load
from refseq import refseq_load
from coordinates import coordinates_from_string

print("Annotator")
query = coordinates_from_string(sys.argv[1])

# db loading
dgv_db = dgv_gold_load()
refseq_db = refseq_load()

# DGV Querying
if query.chr in dgv_db:
    if dgv_db[query.chr].overlaps(query.start, query.end):
        print("Overlap found in DGV")
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
    print("Invalid Chromosome name!")

print("END")
