from intervaltree import IntervalTree


# OMIM DB

def omim_morbid_genes_load():
    chr_dict = {}
    omim_mg_base_path = 'data/20181126_morbidGenes.tsv'
    with open(omim_mg_base_path) as f:
        for line in f:
            parts = line.split('\t')
            pass

    return chr_dict
