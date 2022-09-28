import os.path
import csv

from intervaltree import IntervalTree
from cnvannot.common.serialization import *


# OMIM DB

def omim_morbid_genes_load():
    ddg2p_dict = {}
    hgnc_dict = {}
    chr_dict = {}  # final

    ddg2p_base_file = 'DDG2P_6_5_2022.csv'
    ddg2p_base_path = os.path.join(Common.data_path, ddg2p_base_file)

    hgnc_base_file = 'hgnc_complete_set_2022-04-01.tsv'
    hgnc_base_path = os.path.join(Common.data_path, hgnc_base_file)

    refseq_base_file = 'refGene.txt'
    refseq_base_path = os.path.join(Common.data_path, refseq_base_file)

    final_base = 'coord2genes'

    if serialization_is_serialized(final_base):
        return serialization_deserialize(final_base)

    with open(ddg2p_base_path) as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            if line[0] == 'gene symbol':
                continue
            omim_id = line[1]
            organ_list = line[8].lower()
            if omim_id in ddg2p_dict:
                # Already in list: update.
                ddg2p_dict[omim_id]['organ_list'] += ';' + organ_list
            else:
                ddg2p_dict[omim_id] = {"organ_list": organ_list}

    i = 0
    with open(hgnc_base_path) as f:
        for line in f:
            i = i + 1
            if line.startswith('hgnc_id'):
                continue
            parts = line.split('\t')
            omim_id = parts[31]
            if omim_id == '':
                continue
            refseq_id = parts[23]
            if '.' in parts[23]:
                refseq_id = parts[23].split('.')[0]
            organ_list = ''
            if omim_id in ddg2p_dict:
                organ_list = ddg2p_dict[omim_id]['organ_list']

            data_section = {
                'gene_name': parts[1],
                'full_name': parts[2],
                'gene_aliases': parts[1] + '|' + parts[8][1:-1],
                'organ_list': organ_list
            }
            hgnc_dict[refseq_id] = data_section
            p52split = parts[52].split('|')
            for p in p52split:
                if p.startswith("NM_"):
                    clean_p = p
                    if '.' in p:
                        clean_p = p.split('.')[0]
                    hgnc_dict[clean_p] = data_section

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
                                                   'omim_gene_aliases': hgnc_dict[refseq_id]['gene_aliases'],
                                                   'organ_list': hgnc_dict[refseq_id]['organ_list'],
                                                   'full_data': hgnc_dict[refseq_id]
                                                   }
                except ValueError:
                    pass

    serialization_serialize(chr_dict, final_base)

    return chr_dict
