from intervaltree import IntervalTree


# DGV DB

def refseq_load():
    chr_dict = {}
    dgv_base_path = 'data/refGene.txt'
    with open(dgv_base_path) as f:
        for line in f:
            parts = line.split('\t')
            pass