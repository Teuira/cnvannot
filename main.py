# Annotateur - backend

import sys
from intervaltree import IntervalTree

print("Annotator")
query = sys.argv[1]
query_chr = query.split(':')[0]
query_start_end = query.split(':')[1].split('-')
query_start = int(query_start_end[0])
query_end = int(query_start_end[1])
query_type = query.split(':')[2]

# DGV DB

chrDict = {}

dgv_base_path = 'data/DGV.GS.March2016.50percent.GainLossSep.Final.hg19.gff3'
with open(dgv_base_path) as f:
    for line in f:
        parts = line.split('\t')
        chrom = parts[0]
        start = int(parts[3])
        stop = int(parts[4])
        dat = parts[8]
        dat_parts = dat.split(';')
        var_type = ''
        freq_percent = ''
        for dp in dat_parts:
            if dp.startswith('variant_sub_type'):
                var_type = dp.split('=')[1]
            if dp.startswith('Frequency'):
                freq_percent = float(dp.split('=')[1][:-1])
        if var_type == 'Gain':
            var_type = 'DUP'
        elif var_type == 'Loss':
            var_type = 'DEL'
        if var_type == '':
            print("Cannot parse line")

        if chrom not in chrDict:
            # Add new interval tree as value
            chrDict[chrom] = IntervalTree()

        try:
            chrDict[chrom][start:stop] = {'chr': chrom, 'start': start, 'stop': stop,
                                          'var_type': var_type, 'freq': freq_percent}
        except ValueError:
            pass

if query_chr in chrDict:
    if chrDict[query_chr].overlaps(query_start, query_end):
        print("Overlap found in DGV")
        with open("out.json", "a") as out_file:
            out_file.write('{')
        for r in chrDict[query_chr][query_start:query_end]:
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
