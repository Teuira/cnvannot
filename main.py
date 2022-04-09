# Annotator - backend

import sys
from DGV import dgv_gold_load
from RefSeq import refseq_load

print("Annotator")
query = sys.argv[1]
query_chr = query.split(':')[0]
query_start_end = query.split(':')[1].split('-')
query_start = int(query_start_end[0])
query_end = int(query_start_end[1])
query_type = query.split(':')[2]

dgv_db = dgv_gold_load()
refseq_db = refseq_load()

if query_chr in dgv_db:
    if dgv_db[query_chr].overlaps(query_start, query_end):
        print("Overlap found in DGV")
        with open("out.json", "a") as out_file:
            out_file.write('{')
        for r in dgv_db[query_chr][query_start:query_end]:
            t = r.data['var_type']
            if t != query_type:
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

print("END")
