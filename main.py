# Annotateur - backend

import sys
from intervaltree import Interval, IntervalTree

print("Annotator")
query = sys.argv[1]

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
