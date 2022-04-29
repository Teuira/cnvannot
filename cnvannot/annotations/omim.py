import os.path

from intervaltree import IntervalTree
from cnvannot.common.serialization import *


# OMIM DB

def omim_morbid_genes_load():
    hgnc_dict = {}

    chr_dict = {}  # final

    refseq_base_file = 'refGene.txt'
    refseq_base_path = os.path.join(Common.data_path, refseq_base_file)

    hgnc_base_file = 'hgnc_complete_set_2022-04-01.tsv'
    hgnc_base_path = os.path.join(Common.data_path, hgnc_base_file)

    final_base = 'coord2genes'

    if serialization_is_serialized(final_base):
        return serialization_deserialize(final_base)

    with open(hgnc_base_path) as f:
        for line in f:
            if line.startswith('hgnc_id'):
                continue
            parts = line.split('\t')
            omim_id = parts[31]
            if omim_id == '':
                continue
            refseq_id = parts[23]
            hgnc_dict[refseq_id] = {'gene_aliases': parts[1] + '|' + parts[8]}

    with open(refseq_base_path) as f:
        for line in f:
            parts = line.split('\t')
            refseq_id = parts[1]
            chrom = parts[2]
            start = int(parts[4])
            stop = int(parts[5])
            if refseq_id in hgnc_dict:
                # refSeq id matches with OMIM gene.
                if chrom not in chr_dict:
                    # Add new interval tree as value
                    chr_dict[chrom] = IntervalTree()
                try:
                    chr_dict[chrom][start:stop] = {'chr': chrom, 'start': start, 'stop': stop,
                                                   'omim_gene_aliases': hgnc_dict[refseq_id]['gene_aliases']}
                except ValueError:
                    pass

    serialization_serialize(chr_dict, final_base)

    return chr_dict
